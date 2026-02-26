# Instagram Gemini Bot 🤖

A Python package to build intelligent Instagram DM bots powered by Google Gemini AI. Automatically respond to messages with personalized, context-aware replies.

## Features ✨

- 🤖 **AI-Powered Responses**: Uses Google Gemini for intelligent message generation
- 💬 **Context Memory**: Remembers conversation history for each user
- 🔧 **Easy Configuration**: Simple CLI-based setup
- 🚀 **Production Ready**: Deploy to Azure, AWS, Heroku, or any server
- 📦 **Installable Package**: Install via pip, deploy anywhere
- 🎭 **Customizable Personality**: Define bot behavior with custom instructions
- 🔐 **Secure**: Environment-based configuration
- 📊 **SQLite Storage**: Persistent conversation storage

## Quick Start 🚀

### Installation

```bash
# From PyPI (when published)
pip install instachatdmbot

# Or from source
git clone https://github.com/23f2001706/insta
cd insta
pip install -e .
```

### Setup

1. **Get your credentials**:
   - Instagram: App ID, App Secret from [Meta App Dashboard](https://developers.facebook.com/apps)
   - Gemini: API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)

2. **Initialize the bot** (interactive setup):
   ```bash
   insta-bot init
   ```
   
   This creates a `.env` file with all required configuration.

3. **Verify configuration**:
   ```bash
   insta-bot validate
   ```

4. **Run locally**:
   ```bash
   python main.py
   ```

## Configuration 📋

The bot uses environment variables stored in `.env`:

```env
# Instagram Configuration
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_ACCESS_TOKEN=your_access_token
VERIFY_TOKEN=your_webhook_verify_token
BOT_PAGE_ID=your_page_id
BOT_INSTAGRAM_ID=your_instagram_id

# Gemini Configuration
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.5-flash-lite

# Bot Personality
BOT_NAME=MyBot
BOT_INSTRUCTIONS=You are a helpful Instagram assistant...

# Database
DB_PATH=./conversations.db
```

### Getting Credentials

#### Instagram Credentials

1. Go to [Meta App Dashboard](https://developers.facebook.com/apps)
2. Create or select your app
3. Add Instagram as a product
4. Go to **Settings** → **Basic** to find App ID and App Secret
5. Create a Page Access Token in **Messenger** settings
6. In your app, go to **Messenger** → **Settings** and set webhook URL to:
   ```
   https://yourdomain.com/webhook
   ```

#### Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key to your `.env`

#### Verify Token

Create your own arbitrary token (e.g., `my_super_secret_token_123`) and use the same value in:
- `.env` file as `VERIFY_TOKEN`
- Instagram webhook settings as "Verify Token"

## Usage 📖

### As a Python Package

```python
from insta_bot import InstagramBot

# Create bot with default configurations from .env
bot = InstagramBot()

# Run on port 8000
bot.run(host="0.0.0.0", port=8000)
```

### Custom Configuration

```python
from insta_bot import InstagramBot

# Create with custom instructions
custom_instructions = """
You are a friendly pizza shop assistant.
You help customers order pizza and answer questions.
Keep responses under 100 characters.
"""

bot = InstagramBot(
    custom_instructions=custom_instructions,
    gemini_model="gemini-2.5-flash-lite"
)

bot.run()
```

### CLI Commands

```bash
# Interactive setup
instachatdmbot init

# Validate configuration
instachatdmbot validate

# Run the bot
instachatdmbot run --host 0.0.0.0 --port 8000
```

## Webhook Setup 🔗

### Local Testing with ngrok

```bash
# Install ngrok
pip install ngrok

# In another terminal
ngrok http 8000

# Get the HTTPS URL (e.g., https://abc123.ngrok.io)
```

### Azure Deployment

1. Create Azure App Service (Python 3.10)
2. Configure environment variables in Azure portal
3. Set startup command:
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 main:bot.app
   ```
4. In Instagram settings, set webhook URL to your Azure domain

### AWS Deployment

1. Create AWS Lambda with Python 3.10 runtime
2. Use AWS API Gateway to create HTTP endpoint
3. Set environment variables in Lambda configuration
4. Deploy using `sam` or `serverless` framework

## Project Structure 📁

```
insta-bot-gemini/
├── insta_bot/                 # Main package
│   ├── __init__.py           # Package exports
│   ├── bot.py                # Main bot class
│   ├── config.py             # Configuration management
│   ├── instagram_api.py       # Instagram Graph API wrapper
│   ├── gemini_handler.py      # Gemini AI integration
│   ├── conversation_store.py  # SQLite conversation storage
│   └── cli.py                # CLI commands
├── main.py                    # Entry point
├── setup.py                   # Package setup
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Python dependencies
├── .env.example              # Example configuration
└── README.md                 # This file
```

## How It Works 🔄

```
Instagram DM → Webhook → Bot receives message
  ↓
Bot fetches conversation history from SQLite
  ↓
Message sent to Gemini with system prompt
  ↓
Gemini generates response
  ↓
Response saved to conversation history
  ↓
Response sent back via Instagram API
```

## Example Responses 💬

### Default Assistant
```
User: What's the weather?
Bot: I'm an Instagram assistant, not a weather bot! But I can help with other things. What else can I help with?
```

### Custom: Pizza Shop Bot
```
User: Can I order pizza?
Bot: Absolutely! We have margherita, pepperoni, and more. What size would you like? 🍕
```

## Troubleshooting 🔧

### "403 Forbidden" on webhook verification
- Check `VERIFY_TOKEN` matches in both `.env` and Instagram settings
- Ensure Flask is listening on port 8000

### "Gemini API error"
- Check `GEMINI_API_KEY` is valid and active
- Ensure API is enabled in Google Cloud Console

### "No messages received"
- Check webhook URL is publicly accessible (HTTPS)
- Verify bot has permission to send messages in Meta dashboard
- Check Instagram app ID and access token

### "Messages not stored"
- Check `conversations.db` file is writable
- Ensure SQLite3 is installed: `python -c "import sqlite3"`

## Deployment 🚀

### Heroku

```bash
git push heroku main

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key
heroku config:set INSTAGRAM_ACCESS_TOKEN=your_token
```

### Azure

```bash
az webapp create --name my-bot --resource-group mygroup --plan myplan --runtime python|3.10

# Configure in Azure portal:
# 1. Go to Configuration → Application Settings
# 2. Add all variables from .env
# 3. Save
```

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:bot.app"]
```

## Performance Tips 🏃

1. **Use flash model**: `GEMINI_MODEL=gemini-2.5-flash-lite` (faster, cheaper)
2. **Limit conversation history**: Trim old messages in `conversation_store.py`
3. **Cache responses**: Add Redis for frequently asked questions
4. **Batch responses**: Use quick replies instead of text

## Security ⚠️

- Never commit `.env` file to git (already in `.gitignore`)
- Keep API keys secret
- Use strong `VERIFY_TOKEN`
- Validate webhook signatures (todo)
- Rate-limit responses to prevent abuse

## Contributing 🤝

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License 📄

MIT License - see LICENSE file for details

## Support 💬

- 📖 [Full Documentation](./docs)
- 🐛 [Report Issues](https://github.com/yourusername/insta-bot-gemini/issues)
- 💬 [Discussions](https://github.com/yourusername/insta-bot-gemini/discussions)

## Roadmap 🗺️

- [ ] Rate limiting
- [ ] Webhook signature validation
- [ ] Redis caching
- [ ] Multi-language support
- [ ] Image recognition
- [ ] Admin dashboard
- [ ] Analytics and metrics

---

**Made with ❤️ for Instagram automation**

An automated chatbot for Instagram Direct Messages powered by Google Gemini AI.

## Features

- **Instagram Integration**: Automatically responds to DMs on Instagram
- **Gemini AI**: Leverages Google's Gemini AI for intelligent responses
- **Conversation Memory**: Stores conversation history with users
- **Configurable**: Easy-to-use configuration system

## Setup

### Prerequisites

- Python 3.8+
- Instagram account
- Google Gemini API key

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd insta
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
```bash
# Edit .env file with your credentials
cp .env.example .env
# Edit .env with your Instagram and Gemini API credentials
```

4. Run the application
```bash
python app.py
```

## Configuration

Edit the `.env` file with your settings:

- `INSTAGRAM_USERNAME`: Your Instagram username
- `INSTAGRAM_PASSWORD`: Your Instagram password
- `GEMINI_API_KEY`: Your Google Gemini API key
- `DEBUG`: Enable debug logging (True/False)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, ERROR)

## Project Structure

- `app.py`: Main application entry point
- `config.py`: Configuration management
- `instagram_api.py`: Instagram API wrapper
- `gemini_handler.py`: Gemini AI handler
- `conversation_store.py`: Conversation storage and retrieval
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (keep this private!)

## Usage

The bot will:
1. Listen for incoming Instagram DMs
2. Process each message with Gemini AI
3. Generate personalized responses
4. Store conversation history for context

## License

MIT

## Security Notes

- Never commit `.env` file to version control
- Keep your API keys and passwords secure
- Use environment variables for sensitive data
- OAuth is recommended instead of password-based authentication
