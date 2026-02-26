"""Configuration management for Instagram Gemini Bot"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class - loads from environment variables"""
    
    # Instagram Configuration
    INSTAGRAM_APP_ID = os.getenv("INSTAGRAM_APP_ID")
    INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET")
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_verify_token")
    BOT_PAGE_ID = os.getenv("BOT_PAGE_ID")
    BOT_INSTAGRAM_ID = os.getenv("BOT_INSTAGRAM_ID")
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    
    # Bot Configuration
    BOT_NAME = os.getenv("BOT_NAME", "Assistant")
    BOT_INSTRUCTIONS = os.getenv("BOT_INSTRUCTIONS", "You are a helpful Instagram assistant.")
    
    # API Configuration
    GRAPH_API_URL = "https://graph.instagram.com/v21.0"
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "./conversations.db")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = {
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
            "INSTAGRAM_APP_ID": cls.INSTAGRAM_APP_ID,
            "INSTAGRAM_ACCESS_TOKEN": cls.INSTAGRAM_ACCESS_TOKEN,
            "VERIFY_TOKEN": cls.VERIFY_TOKEN,
        }
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(
                f"❌ Missing required environment variables:\n   " + 
                "\n   ".join(missing) +
                "\n\n📝 Please set these in your .env file"
            )
        
        return True
