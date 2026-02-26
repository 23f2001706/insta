"""Main Instagram Bot class"""
import logging
from flask import Flask, request, jsonify
from .config import Config
from .instagram_api import InstagramAPI
from .gemini_handler import GeminiHandler
from .conversation_store import ConversationStore

logger = logging.getLogger(__name__)


class InstagramBot:
    """Main Instagram Bot with Gemini AI"""
    
    def __init__(self, custom_instructions: str = None, gemini_model: str = None):
        """
        Initialize the bot
        
        Args:
            custom_instructions: Custom system prompt for the AI
            gemini_model: Gemini model to use
        """
        # Validate config
        try:
            Config.validate()
        except ValueError as e:
            logger.error(e)
            raise
        
        # Initialize components
        self.conversation_store = ConversationStore()
        self.instagram_api = InstagramAPI()
        self.gemini_handler = GeminiHandler(
            system_prompt=custom_instructions or Config.BOT_INSTRUCTIONS,
            model=gemini_model or Config.GEMINI_MODEL,
            conversation_store=self.conversation_store
        )
        
        # Flask app
        self.app = Flask(__name__)
        self._setup_routes()
        
        logger.info(f"✅ Bot initialized: {Config.BOT_NAME}")
    
    def _setup_routes(self):
        """Setup Flask webhook routes"""
        
        @self.app.route("/webhook", methods=["GET"])
        def verify_webhook():
            mode = request.args.get("hub.mode")
            token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")
            
            if mode == "subscribe" and token == Config.VERIFY_TOKEN:
                logger.info("✅ Webhook verified!")
                return challenge, 200
            
            logger.warning("❌ Webhook verification failed!")
            return "Forbidden", 403
        
        @self.app.route("/webhook", methods=["POST"])
        def handle_webhook():
            body = request.get_json()
            
            if not body:
                return "Bad Request", 400
            
            if body.get("object") != "instagram":
                return "OK", 200
            
            try:
                for entry in body.get("entry", []):
                    for messaging_event in entry.get("messaging", []):
                        self._handle_message(messaging_event)
                
                return "OK", 200
            except Exception as e:
                logger.error(f"Error handling webhook: {e}")
                return "OK", 200
        
        @self.app.route("/health", methods=["GET"])
        def health():
            return jsonify({"status": "healthy", "bot": Config.BOT_NAME})
    
    def _handle_message(self, messaging_event: dict):
        """Process incoming message and send response"""
        try:
            sender_id = messaging_event.get("sender", {}).get("id")
            recipient_id = messaging_event.get("recipient", {}).get("id")
            timestamp = messaging_event.get("timestamp")
            
            # Skip if this is a message we sent
            if sender_id == Config.BOT_INSTAGRAM_ID:
                return
            
            # Get message
            message = messaging_event.get("message", {})
            user_message = message.get("text")
            
            if not user_message:
                logger.debug(f"Received non-text message from {sender_id}")
                return
            
            logger.info(f"📨 Message from {sender_id}: {user_message}")
            
            # Generate reply
            reply = self.gemini_handler.generate_reply(sender_id, user_message)
            
            # Send reply
            self.instagram_api.send_message(sender_id, reply)
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
        """Run the Flask app"""
        logger.info(f"Starting bot on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)
