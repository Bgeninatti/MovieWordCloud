

from lib.cfg import DB_PATH
from lib.imdb_client import ImdbClient
from lib.logger import get_logger
from lib.models import Movie, init_db, save_imdb_movie

logger = get_logger(__name__)


def download_top_250(imdb_client, excluded_movies_ids):
    top_movies = imdb_client.get_top250(excluded_movies_ids)
    for movie in top_movies:
        save_imdb_movie(movie)


def download_most_populars(imdb_client, excluded_movies_ids):
    popular_movies = imdb_client.get_most_popular_movies(excluded_movies_ids)
    for movie in popular_movies:
        save_imdb_movie(movie)

if __name__ == '__main__':
    init_db(DB_PATH)
    imdb_client = ImdbClient()
    existing_movies = {m.imdb_id for m in Movie.select()}
    download_top_250(imdb_client, existing_movies)
    download_most_populars(imdb_client, existing_movies)
