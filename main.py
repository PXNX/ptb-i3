import logging
import os
from datetime import datetime

from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, filters, CallbackQueryHandler, ConversationHandler, Defaults
from telegram.ext import CommandHandler, MessageHandler

from config import CHANNEL, TOKEN
from messages import append_footer, hello, solution_callback, send_question, QUESTION, PHOTO, SOLUTION, ANSWERS, \
    send_photo, send_solution, send_answers, skip_photo, receive_answer, send_result, cancel

LOG_FILENAME = rf"./logs/{datetime.now().strftime('%Y-%m-%d')}/{datetime.now().strftime('%H-%M-%S')}.log"
os.makedirs(os.path.dirname(LOG_FILENAME), exist_ok=True)
logging.basicConfig(
    format="%(asctime)s %(levelname)-5s %(funcName)-20s [%(filename)s:%(lineno)d]: %(message)s",
    encoding="utf-8",
    filename=LOG_FILENAME,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).build()

    app.add_handler(
        MessageHandler(
            (filters.PHOTO | filters.VIDEO | filters.ANIMATION)
            & filters.Chat(chat_id=CHANNEL), append_footer))

    app.add_handler(CommandHandler("start", hello))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("promote", send_question)],  # filters.Chat(ADMINS)
        states={
            QUESTION: [MessageHandler(filters.TEXT, send_photo)],
            PHOTO: [MessageHandler(filters.PHOTO, send_solution), CommandHandler("skip", skip_photo)],
            SOLUTION: [MessageHandler(filters.TEXT, send_answers)],
            ANSWERS: [CommandHandler("save", send_result), MessageHandler(filters.TEXT, receive_answer), ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    buttons_handler = CallbackQueryHandler(solution_callback)
    app.add_handler(buttons_handler)

    print("### RUN LOCAL ###")
    app.run_polling(poll_interval=1)
