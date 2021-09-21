from telegram import Update
from telegram.ext import CallbackContext
from io import BytesIO
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import re


def args_checker(args):
    if len(args) == 2:
        login = args[0]
        password = args[1]
        if re.match("[a-z]([a-z]|[0-9]|[A-Z]*)", login) and re.match("[a-z]|[0-9]|[A-Z]*", password):
            return True
    return False


def help_command(update: Update, context: CallbackContext) -> None:
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


def start(update: Update, context: CallbackContext) -> None:
    help_command(update, context)


def image_processing(update: Update, context: CallbackContext) -> None:
    img = context.bot.get_file(update.message.photo[-1].file_id)
    file_name = img['file_path'].split('/')[-1]
    print(file_name)
    f = BytesIO(img.download_as_bytearray())
    file_bytes = bytearray(f.read())

    response = requests.post('http://10.91.2.204:5000/api/v1/pictures', files={'image': (file_name, file_bytes)})
    caption = json.loads(response.text)['caption']
    update.message.reply_text(caption, reply_to_message_id=update.message.message_id)


def login_handler(update: Update, context: CallbackContext) -> None:
    args = context.args
    flag = args_checker(args)
    if flag:
        update.message.reply_text("Login successfully")
    else:
        update.message.reply_text("Login should start with lower case English letter and"
                                  " contains only numbers or english letters")


def create_profile_handler(update: Update, context: CallbackContext) -> None:
    args = context.args
    flag = args_checker(args)
    if flag:
        update.message.reply_text("Profile created successfully")
    else:
        update.message.reply_text("Login should start with lower case English letter and"
                                  " contains only numbers or english letters")


def history_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("History replied")
