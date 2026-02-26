import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    INSTAGRAM_APP_ID = os.getenv("INSTAGRAM_APP_ID")
    INSTAGRAM_APP_SECRET = os.getenv("INSTAGRAM_APP_SECRET")
    ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_custom_verify_token_123")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    BOT_NAME = os.getenv("BOT_NAME", "Assistant")
    BOT_PERSONALITY = os.getenv("BOT_PERSONALITY", "You are a helpful Instagram assistant.")

    GRAPH_API_URL = "https://graph.instagram.com/v21.0"

    # ════════════════════════════════════════
    # ADD THESE — critical for preventing echo loops
    # ════════════════════════════════════════
    # Your bot's Instagram page/account ID (the entry.id in webhooks)
    BOT_PAGE_ID = os.getenv("BOT_PAGE_ID", "17841468343963858")
    
    # Your bot's Instagram-scoped user ID (sender.id when bot sends)
    BOT_INSTAGRAM_ID = os.getenv("BOT_INSTAGRAM_ID", "17841468343963858")