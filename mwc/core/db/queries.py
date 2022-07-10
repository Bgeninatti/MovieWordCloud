from peewee import fn

from mwc.core.db.models import Movie


def get_movies_languages():
    return Movie.select().distinct(Movie.original_language)


def get_movies_with_subtitles(language):
    return Movie.select().where(
        Movie.subtitle_id.is_null(False) &
        Movie.original_language == language
    )


def get_existing_tmdb_ids():
    return {m.tmdb_id for m in Movie.select()}


def get_movies_without_subtitles():
    return Movie.select() \
        .where(Movie.subtitle_id.is_null()) \
        .order_by(Movie.popularity.desc())


def get_next_movie():
    movie = Movie.select() \
        .where((Movie.last_tweet.is_null()) & (Movie.subtitle_id.is_null(False))) \
        .order_by(fn.Random()) \
        .first()
    if movie:
        return movie

    movie = Movie.select() \
        .where(Movie.opensubtittle_id.is_null(False)) \
        .order_by(Movie.last_tweet.asc()) \
        .order_by(fn.Random()) \
        .first()
    return movie
