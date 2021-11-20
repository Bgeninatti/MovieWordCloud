import click

from ..cfg import DB_PATH
from ..logger import get_logger
from ..models import Movie, init_db
from .imdb import ImdbClient

logger = get_logger(__name__)


@click.command()
@click.option('--save/--no-save', default=True)
def sync_imdb(save):
    """
    Populates the local databse with movies from an IMDB ranking
    """
    init_db(DB_PATH)
    imdb_client = ImdbClient()
    existing_movies = {m.imdb_id for m in Movie.select()}

    logger.info("Searching new movies in top 250 movies")
    top250_movies = imdb_client.get_top250()
    new_movies = [m for m in top250_movies
                  if m.movieID not in existing_movies]

    logger.info("New movies found: %d", len(new_movies))
    for movie in new_movies:
        Movie.create(
            name=movie,
            year=movie.data.get('year'),
            imdb_id=movie.movieID
        )
