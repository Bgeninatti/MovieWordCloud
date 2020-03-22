import imdb
from helpers import get_top250, get_most_popular_movies_ids
from cfg import DB_PATH
from models import Movie, init_db
from logger import get_logger


logger = get_logger(__name__)


def download_top_250(excluded_movies_ids):
    top_movies = get_top250()
    new_movies = [m for m in top_movies if m.movieID not in excluded_movies_ids]
    logger.info("New movies found in top 250: new_movies=%d", len(new_movies))
    for movie in new_movies:
        year = movie.data.get('year')
        if not year:
            logger.error("Discarding movie: reason='Couldn't find the year in IMDB', name='%s', imdb_id=%s", movie, movie.movieID)
            continue
        logger.info(f"Adding movie to database: name='%s', imdb_id=%s", movie, movie.movieID)
        Movie.create(
            name=movie,
            year=year,
            imdb_id=movie.movieID
        )

def download_most_populars(excluded_movies_ids):
    ia = imdb.IMDb()
    popular_movies = get_most_popular_movies_ids()
    new_movies = [m for m in popular_movies if m not in excluded_movies_ids]
    logger.info("New movies found in most populars: new_movies=%d",
                len(new_movies))
    for m_id in new_movies:
        movie = ia.get_movie(m_id)
        year = movie.data.get('year')
        if not year:
            logger.error("Discarding movie: reason='Couldn't find the year in IMDB', name='%s', imdb_id=%s",
                         movie, movie.movieID)
            continue
        logger.info("Adding movie to database: name='%s', imdb_id=%s",
                    movie, movie.movieID)
        Movie.create(
            name=movie,
            year=movie.data.get('year'),
            imdb_id=movie.movieID
        )


if __name__ == '__main__':
    init_db(DB_PATH)
    existing_movies = {m.imdb_id for m in Movie.select()}
    download_top_250(existing_movies)
    download_most_populars(existing_movies)
