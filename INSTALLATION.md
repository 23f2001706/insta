# Installation Guide 📦

Complete guide to install and run Instagram Gemini Bot.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Meta/Instagram App
- A Google Gemini API key
- Git (optional, for cloning)

## Option 1: Install from PyPI (Recommended)

> Note: This assumes the package is published on PyPI

```bash
pip install insta-bot-gemini
```

Then jump to [Configuration](#configuration)

## Option 2: Install from Source

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/insta-bot-gemini
cd insta-bot-gemini
```

### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install in development mode (editable):

```bash
pip install -e .
```

## Configuration

### 1. Get Your Credentials

#### Instagram Credentials

1. Go to [Meta Developers Dashboard](https://developers.facebook.com/apps/)
2. Create a new app or select existing one
3. Add **Instagram** as a product
4. Under **Settings** → **Basic**, copy:
   - App ID
   - App Secret
5. Go to **Messenger** → **Settings**
6. Generate a **Page Access Token**

#### Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"** in a new project
3. Copy the generated key

#### Verify Token

Create any random string for webhook verification:
```
my_super_secret_token_123
```

### 2. Initialize Bot

Run the interactive initialization:

```bash
insta-bot init
```

This will prompt you for all required values and create a `.env` file.

Or manually create `.env`:

```env
INSTAGRAM_APP_ID=1234567890
INSTAGRAM_APP_SECRET=secret123
INSTAGRAM_ACCESS_TOKEN=token123
VERIFY_TOKEN=my_verify_token
BOT_PAGE_ID=17841414943450863
BOT_INSTAGRAM_ID=17841414943450863
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.5-flash-lite
BOT_NAME=MyBot
BOT_INSTRUCTIONS=You are a helpful Instagram assistant.
```

### 3. Verify Configuration

```bash
insta-bot validate
```

Expected output:
```
✅ Configuration is valid!
  Bot Name: MyBot
  Gemini Model: gemini-2.5-flash-lite
  Page ID: 17841414943450863
```

## Running the Bot

### Local Development

```bash
python main.py
```

Your bot will run on `http://localhost:8000`

### Production with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:bot.app
```

### Using CLI

```bash
insta-bot run --host 0.0.0.0 --port 8000
```

## Setting Up Webhook

### For Local Testing (ngrok)

```bash
# In another terminal, install and run ngrok
pip install pyngrok
ngrok http 8000

# You'll get a URL like: https://abc123d.ngrok.io
```

### Register Webhook with Instagram

1. Go to your App in Meta Dashboard
2. Navigate to **Messenger** → **Settings**
3. Find **Webhooks** section
4. Click **Add Callback URL**
5. Enter:
   - **Callback URL**: `https://yourdomain.com/webhook` (or ngrok URL)
   - **Verify Token**: (the token from your `.env`)
6. Click **Verify and Save**
7. Under **Webhook Fields**, subscribe to:
   - ✅ `messages`
   - ✅ `message_echoes`
   - ✅ `messaging_postbacks`

## Testing the Bot

1. Send a message to your Instagram bot account
2. The bot should reply within a few seconds

Check console output:
```
📨 Message from user_id: Hello!
✅ Message sent to user_id: Hi! How can I help?
```

## Troubleshooting

### ImportError: No module named 'insta_bot'

Make sure you're in the correct directory and virtual environment:

```bash
# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install again
pip install -e .
```

### ModuleNotFoundError: No module named 'flask'

Install requirements:

```bash
pip install -r requirements.txt
```

### "Connection refused" on localhost:8000

- Make sure the bot is running: `python main.py`
- Check if port 8000 is already in use
- Try a different port: `python main.py --port 9000`

### Webhook verification fails (403)

- Check VERIFY_TOKEN matches in `.env` and Instagram settings
- Make sure callback URL is HTTPS (not HTTP)
- Check that your domain/ngrok URL is publicly accessible

### Bot doesn't reply to messages

- Check bot is running and listening
- Verify webhook is registered in Instagram settings
- Check API tokens are valid
- Look at console for error messages

### "Gemini API error: 429"

This means rate limiting. Use the free tier sparingly or upgrade your Gemini API.

## Next Steps

- ✅ Bot is running locally
- 🚀 Deploy to cloud (see [DEPLOYMENT.md](./DEPLOYMENT.md))
- 🎭 Customize bot personality in `.env`
- 📚 Read [README.md](./README.md) for more features

## Getting Help

- Check console logs for error messages
- Run `insta-bot validate` to check configuration
- Review [Troubleshooting](#troubleshooting) section
- Open an issue on GitHub

---

**All set! Your Instagram bot is ready to go! 🚀**
