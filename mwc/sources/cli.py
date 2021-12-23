import click
import logging
from mwc.models import Movie

from mwc.cfg import load_config

from .tmdb import TmdbClient

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
@click.argument('api_key', type=str, default=CONFIG['TMDB_API_KEY'])
def sync_tmdb(api_key):
    """
    Populates the local databse with movies from an IMDB ranking
    """
    tmdb_client = TmdbClient(api_key)
    existing_movies = {m.tmdb_id for m in Movie.select()}

    log.info("Searching most popular movies")
    popular_movies = tmdb_client.get_most_popular(pages=CONFIG['FETCH_RANKING_PAGES'])
    new_movies = [tmdb_id for tmdb_id in popular_movies
                  if tmdb_id not in existing_movies]

    log.info("New movies found: %d", len(new_movies))

    for tmdb_id in new_movies:
        movie = tmdb_client.get_movie(tmdb_id)
        if not movie:
            log.warning("No IMDB Id found for movie: tmdb_id=%s", tmdb_id)
            continue
        movie.save()
