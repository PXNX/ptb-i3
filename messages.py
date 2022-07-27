from telegram import Update
from telegram.ext import CallbackContext

from config import NYX


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi!")


def append_footer(update: Update, _: CallbackContext):
    original_caption = update.channel_post.caption_html_urled if update.channel_post.caption is not None else ''
    update.channel_post.edit_caption(
        f"{original_caption}\n\n👨‍💻 Join <a href='https://t.me/blog_itisinteresting'>IT IS INTERESTING</a> <u>NOW</u> for more!")

def join_member(update: Update, context: CallbackContext):
    context.bot.send_message(NYX, str(update.message.new_chat_members))
