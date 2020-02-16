import datetime
from peewee import (Model, CharField, IntegerField, DateTimeField, SqliteDatabase)

database = SqliteDatabase(None)


class BaseModel(Model):

    class Meta:
        database = database


class Movie(BaseModel):
    name = CharField()
    year = IntegerField()
    imdb_id = CharField(primary_key=True)
    opensubtittle_id = CharField(null=True)
    language_id = CharField(null=True)
    srt_file = CharField(null=True)
    last_upload = DateTimeField(null=True)
    created = DateTimeField(default=datetime.datetime.now)

def init_db(db_path):
    database.init(db_path)
    database.connect()
    database.create_tables([Movie,])
    return database

def get_next_movie():
    movie = Movie.select() \
        .where(Movie.last_upload.is_null()) \
        .order_by(Movie.created.desc()) \
        .first()
    if movie:
        return movie

    movie = Movie.select() \
        .order_by(Movie.last_upload.asc()) \
        .first()
    return movie
