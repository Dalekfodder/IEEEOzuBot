from settings import DB_ADDRESS
from model import Answers, Admins
import peewee


def start_handler_func(bot, update):
    update.message.reply_text(text='ok')


def question_handler_func(bot, update, args):
    for x in set(args):
        db_response = Answers.select().where(Answers.tag == x.lower())
        try:
            db_response.get()
        except Answers.DoesNotExist:
            update.message.reply_text(text='There is no such thing.')
            print("Non Existant Value")
        else:
            final_response = "Answers about " + x.lower() + ":"

            for response in db_response:
                final_response += "\n" + response.answer

            update.message.reply_text(text='{}'.format(final_response))
    print(update.message.from_user)


def is_admin(update):
    user = update.message.from_user.username
    try:
        Admins.select().where(Admins.user_name == user.lower()).get()
    except Admins.DoesNotExist:
        update.message.reply_text(text='You need to be an admin to perform this operation.')
        return False
    return True


def add_admin_handler_func(bot, update, args):
    username = args[0]

    if not is_admin(update):
        return

    try:
        admin = Admins.create(user_name=username, added_by=update.message.from_user.first_name)
        admin.save()
    except peewee.IntegrityError:
        update.message.reply_text(text='Admin already exists.')
        return

    update.message.reply_text(text='Admin added.')


def add_answer_handler(bot, update, args):
    pass


def on_join_handler(bot, update):
    pass


def davet_at(bot, update):
    pass
