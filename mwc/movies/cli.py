import click
import logging

from mwc.cfg import load_config

from .tmdb import TmdbClient
from ..db.queries import get_existing_tmdb_ids

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
@click.argument('api_key', type=str, default=CONFIG['TMDB_API_KEY'])
def sync_tmdb(api_key):
    """
    Populates the local databse with movies from an IMDB ranking
    """
    tmdb_client = TmdbClient(api_key)
    tmdb_ids = get_existing_tmdb_ids()

    fetched_movies = tmdb_client.fetch(pages=CONFIG['FETCH_RANKING_PAGES'])
    new_movies = {
        tmdb_id for tmdb_id in fetched_movies
        if tmdb_id not in tmdb_ids
    }

    log.info("New movies found: %d", len(new_movies))

    for tmdb_id in new_movies:
        movie = tmdb_client.get_movie(tmdb_id)
        if not movie:
            log.warning("No IMDB Id found for movie: tmdb_id=%s", tmdb_id)
            continue
        movie.save()
