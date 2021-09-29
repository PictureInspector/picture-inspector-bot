from telegram_bot import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os


def main():
    # Load environment variables
    load_dotenv()
    # Get bot token from env
    TG_TOKEN = os.getenv('TG_TOKEN')
    # Start the bot
    # Take token and create updater
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher

    # Add methods to dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_processing))
    dispatcher.add_handler(CommandHandler("login", login_handler))
    dispatcher.add_handler(CommandHandler("create", create_profile_handler))
    dispatcher.add_handler(CommandHandler("history", history_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()