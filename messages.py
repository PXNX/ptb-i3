from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes, ConversationHandler
from telethon import TelegramClient

import config

QUESTION, PHOTO, SOLUTION, ANSWERS = range(4)


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

    keyboard = [
        [
            InlineKeyboardButton("Show solution 🧐", callback_data='If you can read this, you\'re gay'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    #    context.bot.send_message(
    #        chat_id=update.effective_chat.id,
    #        text=f'Hello {update.message.chat.first_name}!',
    #        reply_markup=reply_markup,
    #    )

    await update.message.reply_text(f'Tap the button below for solution!', reply_markup=reply_markup)


async def check_member(user_id):
    async with TelegramClient("remove_inactive", config.api_id, config.api_hash) as client:
        return any(member.id == user_id for member in await client.get_participants("blog_itisinteresting"))


async def solution_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    print(query)

    if await check_member(query.from_user.id):
        await query.answer(text=f"Solution: {query.data}", show_alert=True)
    else:
        await query.answer(text=f"Join the channel first!", show_alert=True)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.chat_data['question'] = None
    context.chat_data["photo"] = None
    context.chat_data["solution"] = None
    context.chat_data["answers"] = list()

    await update.message.reply_text("Send your question. You can /cancel at any time.", )

    return QUESTION


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.chat_data["question"] = update.message.text_html_urled

    await update.message.reply_text("Send a photo for your question or tap /skip")

    return PHOTO


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"Photo skipped. Send the detailed solution to your question: {context.chat_data['question']}")

    return SOLUTION


async def send_solution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.chat_data["photo"] = update.message.photo[0]

    await update.message.reply_text(f"Send the detailed solution to your question: {context.chat_data['question']}")

    return SOLUTION


async def send_answers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("send answers")
    context.chat_data["solution"] = update.message.text_html_urled

    await update.message.reply_text(
        "Send short answers to your question, make sure to include the correct one. When done, tap /save")

    return ANSWERS


async def receive_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("receive answer")
    context.chat_data["answers"].append(update.message.text_html_urled)

    return ANSWERS


async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("send result")
    buttons = list()

    for answer in context.chat_data["answers"]:
        buttons.append(
            [
                InlineKeyboardButton(answer, url="https://t.me/blog_itisinteresting")
            ]
        )

    reply_markup = InlineKeyboardMarkup(buttons)
    solution_button = InlineKeyboardMarkup([[
        InlineKeyboardButton("Show solution 🧐", callback_data=context.chat_data["solution"]),
    ]])

    if context.chat_data["photo"] is None:
        await update.message.reply_text(context.chat_data["question"], reply_markup=reply_markup)

        await update.message.reply_text(context.chat_data["question"], reply_markup=solution_button)
    else:
        await update.message.reply_photo(context.chat_data["photo"], context.chat_data["question"],
                                         reply_markup=reply_markup)
        await update.message.reply_photo(context.chat_data["photo"], context.chat_data["question"],
                                         reply_markup=solution_button)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("promotion was cancelled, start new one with /promote")

    return ConversationHandler.END
