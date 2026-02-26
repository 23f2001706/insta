"""Instagram API wrapper for sending and receiving messages"""
import requests
import logging
from .config import Config

logger = logging.getLogger(__name__)


class InstagramAPI:
    """Handle all Instagram Graph API interactions"""
    
    def __init__(self, access_token: str = None):
        self.access_token = access_token or Config.INSTAGRAM_ACCESS_TOKEN
        self.base_url = Config.GRAPH_API_URL
    
    def send_message(self, recipient_id: str, text: str) -> dict:
        """Send a text message to a user"""
        url = f"{self.base_url}/me/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": text},
        }
        params = {"access_token": self.access_token}
        
        try:
            response = requests.post(url, json=payload, params=params, timeout=30)
            response.raise_for_status()
            logger.info(f"✅ Message sent to {recipient_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send message: {e}")
            return {"error": str(e)}
    
    def send_quick_replies(self, recipient_id: str, text: str, replies: list) -> dict:
        """Send message with quick reply buttons"""
        url = f"{self.base_url}/me/messages"
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "text": text,
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": r["title"],
                        "payload": r.get("payload", r["title"]),
                    }
                    for r in replies[:13]  # Max 13 replies
                ],
            },
        }
        params = {"access_token": self.access_token}
        
        try:
            response = requests.post(url, json=payload, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to send quick replies: {e}")
            return {"error": str(e)}
    
    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile information"""
        url = f"{self.base_url}/{user_id}"
        params = {
            "fields": "name,profile_pic",
            "access_token": self.access_token,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Could not fetch profile: {e}")
            return {}
