import os
from config import TOKEN
from messages import start

from telegram import Update  #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext  #upm package(python-telegram-bot)


def help_command(update: Update, context: CallbackContext) -> None:
    htext = '''
Welcome
Send a message to store it.
Send /fetch to retrieve the most recent message'''
    update.message.reply_text(htext)


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
