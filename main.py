import os
from telegram.ext import Application
from handlers import setup_handlers
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

def main():
    """Start the bot.""" 
    app = Application.builder().token(TOKEN).build()

    # Setup handlers
    setup_handlers(app)

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
