"""Gemini AI handler for generating responses"""
import google.generativeai as genai
import logging
from .config import Config
from .conversation_store import ConversationStore

logger = logging.getLogger(__name__)


class GeminiHandler:
    """Handle Gemini AI interactions"""
    
    def __init__(self, system_prompt: str = None, model: str = None, conversation_store: ConversationStore = None):
        """
        Initialize Gemini handler
        
        Args:
            system_prompt: Custom system prompt (instructions for the bot)
            model: Gemini model to use (default: from config)
            conversation_store: Conversation store instance
        """
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = model or Config.GEMINI_MODEL
        self.system_prompt = system_prompt or Config.BOT_INSTRUCTIONS
        self.conversation_store = conversation_store or ConversationStore()
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 500,
            },
        )
        logger.info(f"✅ Gemini initialized with model: {self.model_name}")
    
    def _build_chat_history(self, user_id: str) -> list:
        """Build chat history in Gemini format"""
        history = self.conversation_store.get_history(user_id)
        gemini_history = []
        
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        return gemini_history
    
    def generate_reply(self, user_id: str, user_message: str) -> str:
        """Generate a reply to the user's message"""
        try:
            # Save user message
            self.conversation_store.add_message(user_id, "user", user_message)
            
            # Get conversation history
            chat_history = self._build_chat_history(user_id)
            
            # Remove last message (we just added it) for context window
            if chat_history:
                chat_history = chat_history[:-1]
            
            # Start chat session
            chat = self.model.start_chat(history=chat_history)
            
            # Build prompt with system instructions
            if not chat_history:
                prompt = (
                    f"[SYSTEM INSTRUCTIONS]\n"
                    f"{self.system_prompt}\n"
                    f"[END SYSTEM INSTRUCTIONS]\n\n"
                    f"User message: {user_message}"
                )
            else:
                prompt = user_message
            
            # Generate response
            response = chat.send_message(prompt)
            reply = response.text.strip()
            
            # Clean up any prefixes
            prefixes = ["Reply:", "Response:", "Me:", "Message:", "Him:"]
            for prefix in prefixes:
                if reply.lower().startswith(prefix.lower()):
                    reply = reply[len(prefix):].strip()
            
            # Limit length
            if len(reply) > 990:
                reply = reply[:987] + "..."
            
            # Save bot response
            self.conversation_store.add_message(user_id, "assistant", reply)
            
            return reply
            
        except Exception as e:
            logger.error(f"Error generating reply: {e}")
            return "Sorry, I couldn't generate a response right now. Try again!"
