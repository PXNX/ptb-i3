import os

from telegram.ext import ApplicationBuilder, filters
from telegram.ext import CommandHandler, MessageHandler
from telethon import TelegramClient

import config
from config import CHANNEL, TOKEN
from messages import append_footer, hello

client = TelegramClient("remove_inactive", config.api_id, config.api_hash)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            (filters.PHOTO | filters.VIDEO | filters.ANIMATION)
            & filters.Chat(chat_id=CHANNEL), append_footer))

    app.add_handler(CommandHandler("start", hello))

    app.run_webhook(listen="0.0.0.0",
                    port=
                    int(os.environ["PORT"]),
                    url_path=TOKEN,
                    webhook_url=f"https://ptb-i3.herokuapp.com/{TOKEN}")


if __name__ == '__main__':
    main()
