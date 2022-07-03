from telegram import Update
from telegram.ext import CallbackContext

from constant import FOOTER


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi!")


def append_footer(update: Update, context: CallbackContext):
    original_caption = update.channel_post.caption_html_urled if update.channel_post.caption is not None else ''
    update.channel_post.edit_caption(f"{original_caption}{FOOTER}")
