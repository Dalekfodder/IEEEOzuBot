from settings import DB_ADDRESS
from model import Answers, Admins
import peewee
import telegram
import telegram.ext

def start_handler_func(bot, update):
    update.message.reply_text(text='ok')


def question_handler_func(bot, update, args):
    final_response = ""
    for x in set(args):
        db_response = Answers.select().where(Answers.tag == x.lower())
        try:
            db_response.get()
        except Answers.DoesNotExist:
            print("Non Existant Value")
            continue
        else:
            final_response += "Answers about " + x.lower() + ":"

        for response in db_response:
            final_response += "\n" + response.answer
        final_response += "\n"

    if final_response is not "":
        update.message.reply_text(text='{}'.format(final_response))
    else:
        update.message.reply_text(text='No answers found.')

    print(update.message.from_user)
    print(update.message.chat)


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


def sticker_handler_func(bot, update):
    try:
        bot.delete_message(message_id=update.message.message_id, chat_id=update.message.chat_id)
    except telegram.error.BadRequest:
        bot.sendMessage(chat_id=update.message.from_user['id'], text="atamazki")
        return

    bot.sendMessage(chat_id=update.message.from_user['id'], text="Kardsm stikir atma diyrm")
    print(update.message.from_user)
    print(update.message.chat)


def add_answer_handler_func(bot, update, args):
    tags = args[0].split(",")
    answer = ' '.join(args[1:])
    query = []

    if not is_admin(update):
        return

    for x in tags:
        query.append({'tag': '{}'.format(x), 'answer': '{}'.format(answer)})

    try:
        Answers.insert_many(query).execute()
    except peewee.IntegrityError as err:
        print(err)


def on_join_handler(bot, update):
    pass
