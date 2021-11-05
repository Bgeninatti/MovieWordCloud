import click

from ..cfg import DB_PATH
from ..logger import get_logger
from ..models import Movie, init_db
from .imdb import ImdbClient

logger = get_logger(__name__)


@click.command()
@click.argument('ranking', type=str, default='all', required=True)
@click.option('--save/--no-save', default=True)
def sync_imdb(ranking, save):
    """
    Populates the local databse with movies from an IMDB ranking
    """
    init_db(DB_PATH)
    imdb_client = ImdbClient()
    existing_movies = {m.imdb_id for m in Movie.select()}

    logger.info("Searching new movies: ranking=%s", ranking)
    if ranking == 'top250':
        top250_movies = imdb_client.get_top250()
        new_movies = [m for m in top250_movies
                      if m.movieID not in existing_movies]
    elif ranking == 'most-populars':
        most_popular_ids = imdb_client.get_most_popular_movies_ids()
        new_movies_ids = set(most_popular_ids).difference(existing_movies)
        new_movies = []
        for imdb_id in new_movies_ids:
            new_movies.append(
                imdb_client.get_movie(imdb_id))
    else:
        raise ValueError(f"Ranking not recognized: {ranking}")

    logger.info("New movies found: %d", len(new_movies))
    if save and new_movies:
        for movie in new_movies:
            Movie.create(
                name=movie,
                year=movie.data.get('year'),
                imdb_id=movie.movieID
            )
