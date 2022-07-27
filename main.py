import os

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Defaults

from config import CHANNEL, TOKEN
from messages import start, append_footer, join_member


def main():
    updater = Updater(TOKEN, defaults=Defaults(parse_mode=ParseMode.HTML))

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(
        MessageHandler(
            Filters.update.channel_post &
            (Filters.photo | Filters.video | Filters.animation)
            & Filters.chat(chat_id=CHANNEL), append_footer))

    dp.add_handler(MessageHandler(Filters.all, join_member))

    updater.start_webhook(
        "0.0.0.0",
        int(os.environ["PORT"]),
        TOKEN,
        webhook_url=f"https://ptb-i3.herokuapp.com/{TOKEN}",
    )


if __name__ == '__main__':
    main()
