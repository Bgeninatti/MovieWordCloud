from peewee import fn

from mwc.db.models import Movie, log


def get_all_movies_with_subtitles():
    return Movie.select() \
        .where(Movie.opensubtittle_id.is_null(False) & Movie.srt_file.is_null(False))


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


def get_or_create_by_imdb_movie(imdb_movie):
    movie = Movie.select().where(Movie.imdb_id == imdb_movie.movieID).first()
    log.info(
        "Searching IMDB movie in database: name='%s', imdb_id=%s",
        imdb_movie,
        imdb_movie.movieID
    )
    if movie:
        log.info(
            "IMDB movie found in database: name='%s', imdb_id=%s",
            imdb_movie,
            imdb_movie.movieID
        )
        return movie

    year = imdb_movie.data.get('year')
    if not year:
        log.error(
            "Error adding movie to database: reason='%s', name='%s', imdb_id=%s",
            "Couldn't find the year in IMDB",
            imdb_movie,
            imdb_movie.movieID
        )
        return
    log.info(
        "Adding movie to database: name='%s', imdb_id=%s",
        imdb_movie,
        imdb_movie.movieID
    )
    return Movie.create(
        name=imdb_movie,
        year=imdb_movie.data.get('year'),
        imdb_id=imdb_movie.movieID
    )
