from telegram import Update
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, Filters
from io import BytesIO
from dotenv import load_dotenv
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import re
import os
load_dotenv()


# Main bot class
class PicTexBot:
    # Init function
    def __init__(self, token):
        # Take token and create updater
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

        # Add methods to dispatcher
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.image_processing))
        self.dispatcher.add_handler(CommandHandler("login", self.login_handler))
        self.dispatcher.add_handler(CommandHandler("create", self.create_profile_handler))
        self.dispatcher.add_handler(CommandHandler("history", self.history_handler))

        self.updater.start_polling()
        self.updater.idle()

    # Method for checking login and password arguments
    @staticmethod
    def args_checker(args):
        # If passed exactly 2 arguments: login and password
        if len(args) == 2:
            login = args[0]
            password = args[1]
            # If matched the re
            if re.match("[a-z]([a-z]|[0-9]|[A-Z]*)", login) and re.match("[a-z]|[0-9]|[A-Z]*", password):
                return True
        return False

    # Method for /help command
    @staticmethod
    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Welcome to SSAD project PicTex by:\n\n"
                                  "Dinislam Gabitov\n"
                                  "Andreay Palaev\n"
                                  "Georgy Andryushenko\n"
                                  "Roman Nabuillin\n"
                                  "\n"
                                  "This bot generates caption for a image.\n"
                                  "\n"
                                  "Commands:\n\n"
                                  "/help - help message\n"
                                  "/create <login> <password> - create an account\n"
                                  "/login <login> <password> - login to account\n"
                                  "/history - view history\n"
                                  "Send image to receive a caption")

    # Method for /start command
    def start(self, update: Update, context: CallbackContext) -> None:
        self.help_command(update, context)

    # Method if image was sent to the bot
    @staticmethod
    def image_processing(update: Update, context: CallbackContext) -> None:
        # Get image from the bot
        img = context.bot.get_file(update.message.photo[-1].file_id)
        file_name = img['file_path'].split('/')[-1]
        f = BytesIO(img.download_as_bytearray())
        file_bytes = bytearray(f.read())

        # Send image to the server
        SERVER_ADDR = os.getenv("SERVER_ADDR")
        response = requests.post(SERVER_ADDR, files={'image': (file_name, file_bytes)})
        # Receive caption from server
        caption = json.loads(response.text)['caption']
        update.message.reply_text(caption, reply_to_message_id=update.message.message_id)

    # Mathod for /login command handle
    # TODO make login
    def login_handler(self, update: Update, context: CallbackContext) -> None:
        args = context.args
        flag = self.args_checker(args)
        if flag:
            update.message.reply_text("Login successfully")
        else:
            update.message.reply_text("Login should start with lower case English letter and"
                                      " contains only numbers or english letters")

    # Method for /create command handle
    # TODO Make create
    def create_profile_handler(self, update: Update, context: CallbackContext) -> None:
        args = context.args
        flag = self.args_checker(args)
        if flag:
            update.message.reply_text("Profile created successfully")
        else:
            update.message.reply_text("Login should start with lower case English letter and"
                                      " contains only numbers or english letters")

    # Method for /history command handle
    # TODO Make history
    @staticmethod
    def history_handler(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("History replied")
