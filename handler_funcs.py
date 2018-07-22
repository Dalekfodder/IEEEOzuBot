import sqlite3
import dbconnection as db


def start_handler_func(bot, update):
    update.message.reply_text(text='ok')


def question_handler_func(bot, update, args):
    conn = db.DbConnection('cevap.db')

    final_response = ""

    for x in args:
        try:
            conn.cursor.execute('''SELECT answers.cevap FROM answers WHERE tags=? ''', [x])
        except sqlite3.Error as err:
            print(err)

        response1 = conn.cursor.fetchone()
        if response1 is not None:
            final_response += response1[0]
            print(final_response)

    if final_response is not "":
        update.message.reply_text(text='{}'.format(final_response))
    else:
        update.message.reply_text(text='öyle bişe yog')

    print(update.message.from_user)


def add_question_handler(bot, update, args):
    pass


def authorize_handler(bot, update, args):
    pass


def sticker_handler(bot, update):
    pass


def on_join_handler(bot, update):
    pass


def davet_at(bot, update):
    pass
