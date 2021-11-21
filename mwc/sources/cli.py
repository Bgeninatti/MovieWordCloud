import click
import logging
from mwc.models import Movie

from .imdb import ImdbClient

log = logging.getLogger(__name__)


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
