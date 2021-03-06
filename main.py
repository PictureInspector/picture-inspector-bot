from telegram_bot import start, help_command, image_processing
from telegram_bot import handle_text, handle_callback
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from dotenv import load_dotenv
import os


load_dotenv()


if __name__ == '__main__':
    
    # Get bot token from env
    TG_TOKEN = os.getenv('TG_TOKEN')
    
    # Start the bot
    # Take token and create updater
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher

    IMAGE_FILTER = Filters.photo | Filters.document.category("image")

    # Add methods to dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(IMAGE_FILTER, image_processing))
    dispatcher.add_handler(MessageHandler(~IMAGE_FILTER, handle_text))
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    updater.idle()
