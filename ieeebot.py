from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from handler_funcs import *

updater = Updater(token='585898772:AAFc5v96G4EBEs1fhP6xKMiufaN3XY5XaFM')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

question_handler = CommandHandler('soru', question_handler_func, pass_args=True)
start_handler = CommandHandler('start', start_handler_func)

dispatcher.add_handler(question_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()