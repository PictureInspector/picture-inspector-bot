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

SERVER_ADDR = os.getenv("SERVER_ADDR")


def handle_callback(update: Update, context: CallbackContext) -> None:
    """
    This method handles the user feedback. If a user presses either of  👍 👎
    buttons, the feedback for the image caption will be sent to the server.
    """

    callback_data_list = json.loads(update.callback_query.data)
    feedback = {
        "image_url": callback_data_list[1],
        "is_good": callback_data_list[0]
    }

    try:
        response = requests.post(
            f"https://{SERVER_ADDR}/api/v1/feedback",
            data=feedback,
            verify="./cert.pem"
        )
    except Exception as exc:
        context.bot.answer_callback_query(
            callback_query_id=update.callback_query.id,
            text='Oops... Somehow we cannot save your feedback 😔'
        )
        raise exc

    if response.ok:
        if response.text == 'already saved':
            callback_answer_text = "We've already got your feedback 😏"
        else:
            callback_answer_text = 'Thank you for feedback!'
    else:
        callback_answer_text = 'Oops... Somehow we cannot save your feedback 😔'

    context.bot.answer_callback_query(
        callback_query_id=update.callback_query.id,
        text=callback_answer_text
    )


def handle_text(update: Update, context: CallbackContext) -> None:
    """
    This function is triggered if a user sends any text message.
    The bot will ask a user to send an image.
    """
    update.message.reply_text("No, you have to send an _image_",
                              parse_mode='Markdown')


def help_command(update: Update, context: CallbackContext) -> None:
    """
    This function will print
    'Send an image to receive a text'
    for the '\help' command.
    """
    update.message.reply_text("Send an image to receive a text")


def start(update: Update, context: CallbackContext) -> None:
    """
    This function will be called for the 'start' command.
    It duplicates the '\help' command.
    """
    help_command(update, context)


def image_processing(update: Update, context: CallbackContext) -> None:
    """
    This method is triggered when a user sends an image to the bot.
    The image will be sent to the server for caption generating.
    After that an image caption will be returned back to the user.
    """

    # Get image from the bot
    img = context.bot.get_file(update.message.photo[-1].file_id)
    file_name = img['file_path'].split('/')[-1]
    f = BytesIO(img.download_as_bytearray())
    file_bytes = bytearray(f.read())

    # Send image to the server
    try:
        response = requests.post(
            f"https://{SERVER_ADDR}/api/v1/pictures",
            files={'image': (file_name, file_bytes)},
            verify="./cert.pem"
        )
    except Exception as exc:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Couldn't process your image 😔\nPlease send the image again"
        )
        raise exc

    # Receive caption from server
    image_url = json.loads(response.text)['imageURL']
    caption = json.loads(response.text)['caption']

    # Reply the user with the caption and the buttons to rate the caption
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=caption,
        reply_to_message_id=update.message.message_id,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "👍",
                        callback_data=json.dumps(["1", image_url])
                    ),
                    InlineKeyboardButton(
                        "👎",
                        callback_data=json.dumps(["0", image_url])
                    )
                ]
            ]
        )
    )
