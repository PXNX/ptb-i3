import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, filters
from telegram.ext import CommandHandler, MessageHandler
from telethon import TelegramClient

import config
from config import CHANNEL, TOKEN
from messages import append_footer


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    is_member = await check_member(update.message.from_user.id)

    await update.message.reply_text(f"is member of i3: {is_member}")


async def check_member(user_id):
    async with TelegramClient("remove_inactive", config.api_id, config.api_hash) as client:

        async for member in client.iter_participants("blog_itisinteresting"):
            print(member.id)
            if member.id == user_id: return True
        return False


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            (filters.PHOTO | filters.VIDEO | filters.ANIMATION)
            & filters.Chat(chat_id=CHANNEL), append_footer))

    app.add_handler(CommandHandler("start", hello))

    app.run_webhook("0.0.0.0",
                    int(os.environ["PORT"]),
                    webhook_url=f"https://ptb-i3.herokuapp.com/{TOKEN}")


if __name__ == '__main__':
    main()
