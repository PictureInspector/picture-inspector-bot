from telegram_bot import PicTexBot
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    TG_TOKEN = os.getenv('TG_TOKEN')

    bot = PicTexBot(TG_TOKEN)


if __name__ == '__main__':
    main()