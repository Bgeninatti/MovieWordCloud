import datetime
from peewee import (Model, CharField, DateTimeField, SqliteDatabase, CompositeKey)

database = SqliteDatabase(None)


class BaseModel(Model):

    class Meta:
        database = database


class Movie(BaseModel):
    name = CharField()
    imdb_id = CharField()
    opensubtittle_id = CharField()
    language_id = CharField()
    srt_file = CharField()
    last_upload = DateTimeField(null=True)

    class Meta:
        primary_key = CompositeKey('imdb_id', 'opensubtittle_id')


def init_db(db_path):
    database.init(db_path)
    database.connect()
    database.create_tables([Movie,])
    return database