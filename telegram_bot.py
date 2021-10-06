from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import Update
from telegram.ext import CallbackContext
from io import BytesIO
from dotenv import load_dotenv
import json
import requests
import os
load_dotenv()


def handle_callback(update: Update, context: CallbackContext) -> None:

    if update.callback_query.data == "like":
        print('liked')
    elif update.callback_query.data == "dislike":
        print('disliked')
    
    context.bot.answer_callback_query(update.callback_query.id)


def handle_text(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("No, you have to send an _image_", parse_mode='Markdown')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send an image to receive a text")


# Method for /start command
def start(update: Update, context: CallbackContext) -> None:
    help_command(update, context)


# Method if image was sent to the bot
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

    # reply the user with the caption and the buttons to rate the caption
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption,
        reply_to_message_id=update.message.message_id,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👍", callback_data='like'),
                    InlineKeyboardButton("👎", callback_data='dislike')
                ]
            ]
        )
    )
