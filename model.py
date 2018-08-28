import peewee

from settings import DB_ADDRESS

db = peewee.SqliteDatabase(DB_ADDRESS)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Answers(BaseModel):
    category_name = peewee.TextField()
    tag_name = peewee.TextField()
    answer = peewee.TextField()


class Admins(BaseModel):
    user_name = peewee.TextField(unique=True)
    added_by = peewee.TextField()


if __name__ == '__main__':
    try:
        Answers.create_table()
        Admins.create_table()
    except peewee.OperationalError as err:
        print(err)