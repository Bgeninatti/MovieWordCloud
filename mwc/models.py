import datetime

from peewee import (CharField, DateTimeField, IntegerField, Model,
                    SqliteDatabase, fn)

from .logger import get_logger

logger = get_logger(__name__)
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

def save_imdb_movie(imdb_movie):
    year = imdb_movie.data.get('year')
    if not year:
        raise ValueError("Couldn't find the year in IMDB")
    logger.info("Adding movie to database: name='%s', imdb_id=%s",
                imdb_movie, imdb_movie.movieID)
    Movie.create(
        name=imdb_movie,
        year=imdb_movie.data.get('year'),
        imdb_id=imdb_movie.movieID
    )
