"""
Instagram Gemini Bot - Main entry point

Run this file to start your bot:
    python main.py
"""

from insta_bot.bot import InstagramBot
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # Create bot with default configuration from .env
    bot = InstagramBot()
    
    # Run on port 8000
    # For production, use gunicorn: gunicorn -w 4 -b 0.0.0.0:8000 main:bot.app
    bot.run(host="0.0.0.0", port=8000, debug=False)
