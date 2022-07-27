from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from telethon import TelegramClient

import config
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi!")


async def append_footer(update: Update, _: CallbackContext):
    original_caption = update.channel_post.caption_html_urled if update.channel_post.caption is not None else ''
    await update.channel_post.edit_caption(
        f"{original_caption}\n\n👨‍💻 Join <a href='https://t.me/blog_itisinteresting'>IT IS INTERESTING</a> <u>NOW</u> for more!")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    is_member = await check_member(update.message.from_user.id)

    await update.message.reply_text(f"is member of i3: {is_member}")


async def check_member(user_id):
    async with TelegramClient("remove_inactive", config.api_id, config.api_hash) as client:
        return any(member.id == user_id for member in await client.get_participants("blog_itisinteresting"))
