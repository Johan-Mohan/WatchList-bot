# bot/main.py

import os
import logging
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FRONTEND_URL = os.getenv("FRONTEND_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sends a message with a button that opens the web app.
    """
    await context.bot.set_chat_menu_button(
        chat_id=update.effective_chat.id,
        menu_button=MenuButtonWebApp(text="Open Movie Tracker", web_app=WebAppInfo(url=FRONTEND_URL))
    )
    await update.message.reply_text(
        "Welcome to the Movie Tracker Bot! Click the menu button below to open the app."
    )

def main() -> None:
    """
    Run the bot.
    """
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
