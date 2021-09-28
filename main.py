from telegram_bot import PicTexBot
from dotenv import load_dotenv
import os


def main():
    # Load environment variables
    load_dotenv()
    # Get bot token from env
    TG_TOKEN = os.getenv('TG_TOKEN')
    # Start the bot
    PicTexBot(TG_TOKEN)


if __name__ == '__main__':
    main()