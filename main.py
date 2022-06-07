import os
from config import TOKEN, CHANNEL
from messages import start, append_footer

from telegram import Update, ParseMode  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults, CallbackContext  #upm package(python-telegram-bot)


def main():
    updater = Updater(TOKEN, defaults=Defaults(parse_mode=ParseMode.HTML))

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(
        MessageHandler(
            Filters.update.channel_post &
            (Filters.photo | Filters.video | Filters.animation)
            & Filters.chat(chat_id=CHANNEL), append_footer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
