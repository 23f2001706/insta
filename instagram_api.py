import requests
from config import Config


class InstagramAPI:
    def __init__(self):
        self.base_url = Config.GRAPH_API_URL
        self.access_token = Config.ACCESS_TOKEN

    def send_text_message(self, recipient_id: str, message_text: str) -> dict:
        """Send a text message to a user via Instagram DM."""
        url = f"{self.base_url}/me/messages"

        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text},
        }

        params = {"access_token": self.access_token}

        try:
            response = requests.post(url, json=payload, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Message sent to {recipient_id}: {result}")
            return result
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send message to {recipient_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text}")
            return {"error": str(e)}

    def send_quick_replies(self, recipient_id: str, message_text: str, 
                           quick_replies: list[dict]) -> dict:
        """Send a message with quick reply buttons."""
        url = f"{self.base_url}/me/messages"

        # Instagram quick replies format
        payload = {
            "recipient": {"id": recipient_id},
            "message": {
                "text": message_text,
                "quick_replies": [
                    {
                        "content_type": "text",
                        "title": qr["title"],
                        "payload": qr.get("payload", qr["title"]),
                    }
                    for qr in quick_replies[:13]  # Max 13 quick replies
                ],
            },
        }

        params = {"access_token": self.access_token}

        try:
            response = requests.post(url, json=payload, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to send quick replies: {e}")
            return {"error": str(e)}

    def get_user_profile(self, user_id: str) -> dict:
        """Get user's profile info (name, profile pic)."""
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
            print(f"Could not fetch profile for {user_id}: {e}")
            return {}

    def set_ice_breakers(self, ice_breakers: list[dict]) -> dict:
        """Set ice breaker questions that appear when user opens chat."""
        url = f"{self.base_url}/me/messenger_profile"

        payload = {
            "ice_breakers": [
                {
                    "question": ib["question"],
                    "payload": ib.get("payload", ib["question"]),
                }
                for ib in ice_breakers[:4]  # Max 4 ice breakers
            ]
        }

        params = {"access_token": self.access_token}

        try:
            response = requests.post(url, json=payload, params=params, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to set ice breakers: {e}")
            return {"error": str(e)}


# Singleton
instagram_api = InstagramAPI()