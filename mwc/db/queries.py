from peewee import fn

from mwc.db.models import Movie


def get_all_movies_with_subtitles():
    return Movie.select() \
        .where(Movie.opensubtittle_id.is_null(False) & Movie.srt_file.is_null(False))


def get_all_tmdb_ids():
    return {m.tmdb_id for m in Movie.select()}


def get_movies_without_subtitles():
    return Movie.select().where(Movie.opensubtittle_id.is_null())


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
        .order_by(Movie.last_upload.asc()) \
        .order_by(fn.Random()) \
        .first()
    return movie
