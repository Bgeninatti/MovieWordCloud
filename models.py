import datetime
from peewee import (Model, CharField, IntegerField, DateTimeField, SqliteDatabase, fn)

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

def get_next_movie(imdb_id=None):
    if imdb_id:
        movie = Movie.select().where(Movie.imdb_id == imdb_id).first()
        return movie

    movie = Movie.select() \
        .where((Movie.last_upload.is_null()) & (Movie.opensubtittle_id.is_null(False))) \
        .order_by(fn.Random()) \
        .first()
    if movie:
        return movie

    movie = Movie.select() \
        .where(Movie.opensubtittle_id.is_null(False)) \
        .order_by(Movie.last_upload.asc())[:10] \
        .order_by(fn.Random()) \
        .first
    return movie
