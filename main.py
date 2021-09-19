from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram_bot import *
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    TG_TOKEN = os.getenv('TG_TOKEN')

    updater = Updater(TG_TOKEN)

    dispatcher = updater.dispatcher

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