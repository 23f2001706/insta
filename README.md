# Instagram Gemini Bot

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
