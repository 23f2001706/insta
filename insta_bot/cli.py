"""CLI tool for initializing and managing the bot"""
import os
import sys
import click
from pathlib import Path


@click.group()
def cli():
    """Instagram Gemini Bot CLI"""
    pass


@cli.command()
def init():
    """Initialize a new bot project"""
    click.echo("🤖 Instagram Gemini Bot - Project Initializer")
    click.echo("=" * 50)
    
    # Check if .env exists
    if Path(".env").exists():
        if not click.confirm("⚠️  .env already exists. Overwrite?"):
            click.echo("❌ Cancelled")
            return
    
    # Gather information
    click.echo("\n📝 Instagram Configuration:")
    app_id = click.prompt("  Instagram App ID", type=str)
    app_secret = click.prompt("  Instagram App Secret", type=str)
    access_token = click.prompt("  Instagram Access Token", type=str)
    verify_token = click.prompt("  Verify Token (for webhook)", type=str, default="my_verify_token")
    page_id = click.prompt("  Bot Page ID", type=str)
    bot_ig_id = click.prompt("  Bot Instagram ID", type=str)
    
    click.echo("\n🤖 Gemini Configuration:")
    gemini_key = click.prompt("  Gemini API Key", type=str, hide_input=True)
    gemini_model = click.prompt("  Gemini Model", type=str, default="gemini-2.5-flash-lite")
    
    click.echo("\n🎭 Bot Personality:")
    bot_name = click.prompt("  Bot Name", type=str, default="Assistant")
    click.echo("  Enter bot instructions (what the bot should do):")
    click.echo("  (Tip: You can use multi-line input. Press Enter twice to finish)")
    
    instructions = []
    while True:
        try:
            line = input()
            if line == "":
                if instructions and instructions[-1] == "":
                    instructions.pop()
                    break
                instructions.append("")
            else:
                instructions.append(line)
        except EOFError:
            break
    
    bot_instructions = "\n".join(instructions).strip()
    if not bot_instructions:
        bot_instructions = "You are a helpful Instagram assistant. Keep responses concise (under 1000 chars)."
    
    # Create .env
    env_content = f"""# Instagram Configuration
INSTAGRAM_APP_ID={app_id}
INSTAGRAM_APP_SECRET={app_secret}
INSTAGRAM_ACCESS_TOKEN={access_token}
VERIFY_TOKEN={verify_token}
BOT_PAGE_ID={page_id}
BOT_INSTAGRAM_ID={bot_ig_id}

# Gemini Configuration
GEMINI_API_KEY={gemini_key}
GEMINI_MODEL={gemini_model}

# Bot Configuration
BOT_NAME={bot_name}
BOT_INSTRUCTIONS={bot_instructions}

# Database
DB_PATH=./conversations.db
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    click.secho("✅ .env file created successfully!", fg="green")
    click.echo("\n📋 Next steps:")
    click.echo("  1. Install dependencies: pip install insta-bot")
    click.echo("  2. Run the bot: python main.py")
    click.echo("  3. Set your Instagram webhook URL to: https://yourdomain.com/webhook")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to run on")
@click.option("--port", default=8000, help="Port to run on")
def run(host, port):
    """Run the bot"""
    from .bot import InstagramBot
    
    try:
        bot = InstagramBot()
        click.echo(f"🚀 Running on {host}:{port}")
        bot.run(host=host, port=port)
    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        sys.exit(1)


@cli.command()
def validate():
    """Validate configuration"""
    from .config import Config
    
    try:
        Config.validate()
        click.secho("✅ Configuration is valid!", fg="green")
        click.echo(f"  Bot Name: {Config.BOT_NAME}")
        click.echo(f"  Gemini Model: {Config.GEMINI_MODEL}")
        click.echo(f"  Page ID: {Config.BOT_PAGE_ID}")
    except ValueError as e:
        click.secho(f"❌ Configuration error: {e}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    cli()
