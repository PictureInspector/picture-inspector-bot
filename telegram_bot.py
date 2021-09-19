from telegram import Update
from telegram.ext import CallbackContext
import re


def args_checker(args):
    if len(args) == 2:
        login = args[0]
        password = args[1]
        if re.match("[a-z]([a-z]|[0-9]|[A-Z]*)", login) and re.match("[a-z]|[0-9]|[A-Z]*", password):
            return True
    return False


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
                              " sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. ")


def start(update: Update, context: CallbackContext) -> None:
    help_command(update, context)


def image_processing(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("There should be a caption")


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
