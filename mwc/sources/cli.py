import click
import logging
from mwc.models import Movie

from mwc.cfg import load_config

from .imdb import ImdbClient
from .tmdb import TmdbClient

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
def sync_imdb():
    """
    Populates the local databse with movies from an IMDB ranking
    """
    imdb_client = ImdbClient()
    existing_movies = {m.imdb_id for m in Movie.select()}

    log.info("Searching new movies in top 250 movies")
    top250_movies = imdb_client.get_top250()
    new_movies = [m for m in top250_movies
                  if m.movieID not in existing_movies]

    log.info("New movies found: %d", len(new_movies))
    for movie in new_movies:
        Movie.create(
            name=movie,
            year=movie.data.get('year'),
            imdb_id=movie.movieID
        )

@click.command()
@click.argument('api_key', type=str, default=CONFIG['TMDB_API_KEY'])
def sync_tmdb(api_key):
    """
    Populates the local databse with movies from an IMDB ranking
    """
    tmdb_client = TmdbClient(api_key)
    existing_movies = {m.tmdb_id for m in Movie.select()}

    log.info("Searching most popular movies")
    popular_movies = tmdb_client.get_most_popular()
    new_movies = [tmdb_id for tmdb_id in popular_movies
                  if tmdb_id not in existing_movies]

    log.info("New movies found: %d", len(new_movies))

    for tmdb_id in new_movies:
        movie = tmdb_client.get_movie(tmdb_id)
        movie.save()
