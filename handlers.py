import peewee
import telegram
import telegram.ext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import run_async, ConversationHandler

from model import Answers, Admins

CATEGORIES, TAGS = range(2)


@run_async
def question_handler(bot, update):
    category_list = Answers.select(Answers.category_name).distinct()
    button_list = [[InlineKeyboardButton(category.category_name, callback_data="cat" + category.category_name)] for
                   category in category_list]
    button_list.append([InlineKeyboardButton("Bu listede yok.", callback_data="yok")])
    reply_markup = InlineKeyboardMarkup(button_list)

    update.message.reply_text(text="Hangi konuda yardım almak istiyorsun?",
                              reply_markup=reply_markup)
    return CATEGORIES


@run_async
def callback_handler_back(bot, update):
    callback = update.callback_query

    category_list = Answers.select(Answers.category_name).distinct()
    button_list = [[InlineKeyboardButton(category.category_name, callback_data="cat" + category.category_name)] for
                   category in category_list]
    button_list.append([InlineKeyboardButton("Bu listede yok.", callback_data="yok")])
    reply_markup = InlineKeyboardMarkup(button_list)

    callback.edit_message_text(text="Hangi konuda yardım almak istiyorsun?", reply_markup=reply_markup)
    bot.answer_callback_query(callback_query_id=callback.id)

    return CATEGORIES


@run_async
def callback_handler_categories(bot, update):
    callback = update.callback_query
    data = callback.data[3:]

    tag_list = Answers.select(Answers.tag_name).where(Answers.category_name == data).distinct()
    button_list = [[InlineKeyboardButton(tag.tag_name, callback_data="tag" + tag.tag_name)] for tag in tag_list]
    button_list.append([InlineKeyboardButton("Geri git.", callback_data="geri")])
    reply_markup = InlineKeyboardMarkup(button_list)

    callback.edit_message_text(text="Hangi " + data + " hakkında bilgi almak istersin?", reply_markup=reply_markup)

    return TAGS


@run_async
def callback_handler_tags(bot, update):
    callback = update.callback_query
    data = callback.data[3:]
    reply_text = ""

    answers_list = Answers.select(Answers.answer).where(Answers.tag_name == data)
    for x in answers_list:
        reply_text += "\n" + x.answer
    callback.edit_message_text(text=reply_text)
    bot.answer_callback_query(callback_query_id=callback.id)

    return ConversationHandler.END


@run_async
def callback_handler_custom_question(bot, update):
    print("ok")
    callback = update.callback_query
    bot.answer_callback_query(callback_query_id=callback.id)
    return ConversationHandler.END


# Supposed to handle the custom question option in the main menu


@run_async
def is_admin(update):
    user = update.message.from_user.username
    try:
        Admins.select().where(Admins.user_name == user.lower()).get()
    except Admins.DoesNotExist:
        update.message.reply_text(text='You need to be an admin to perform this operation.')
        return False
    return True


@run_async
def add_admin_handler(bot, update, args):
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


@run_async
def sticker_handler(bot, update):
    try:
        bot.delete_message(message_id=update.message.message_id, chat_id=update.message.chat_id)
    except telegram.error.BadRequest:
        bot.sendMessage(chat_id=update.message.from_user['id'], text="hadi gruba at")
        return

    bot.sendMessage(chat_id=update.message.from_user['id'], text="Kardsm stikir atma diyrm")
    print(update.message.from_user)
    print(update.message.chat)


@run_async
def add_answer_handler(bot, update, args):
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
