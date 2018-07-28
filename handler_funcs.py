from settings import DB_ADDRESS
from model import Answers, Admins
import peewee


def start_handler_func(bot, update):
    update.message.reply_text(text='ok')


def question_handler_func(bot, update, args):
    final_response = ""

    for x in args:
        db_response = Answers.select().where(Answers.tag == x)
        try:
            db_response.get()
        except Answers.DoesNotExist:
            print("Non Existant Value")
        else:
            final_response += "Answers about " + x + ":"

            for response in db_response:
                final_response += "\n" + response.answer
                print(response)


    if final_response is not "":
        update.message.reply_text(text='{}'.format(final_response))
    else:
        update.message.reply_text(text='Non Existant Value')

    print(update.message.from_user)


def add_admin_handler_func(bot, update, args):
    pass


def add_answer_handler(bot, update, args):
    pass


def on_join_handler(bot, update):
    pass


def davet_at(bot, update):
    pass
