import click
import logging

from mwc.core.cfg import load_config
from .service import MoviesService

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
@click.argument('api_key', type=str, default=CONFIG['TMDB_API_KEY'])
@click.argument('pages', type=int, default=CONFIG['FETCH_RANKING_PAGES'])
def sync_tmdb(api_key, pages):
    """
    Populates the local databse with new movies
    """
    service = MoviesService(tmdb_api_key=api_key, fetch_ranking_pages=pages)
    service.sync()
