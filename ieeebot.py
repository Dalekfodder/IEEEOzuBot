from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from handler_funcs import *
from settings import BOT_TOKEN

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

question_handler = CommandHandler('soru', question_handler_func, pass_args=True)
start_handler = CommandHandler('start', start_handler_func)
add_admin_handler = CommandHandler('adminekle', add_admin_handler_func, pass_args=True)
add_answer_handler = CommandHandler('soruekle', add_answer_handler_func, pass_args=True)
sticker_handler = MessageHandler(Filters.sticker, sticker_handler_func)


dispatcher.add_handler(question_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_admin_handler)
dispatcher.add_handler(sticker_handler)
dispatcher.add_handler(add_answer_handler)

updater.start_polling()