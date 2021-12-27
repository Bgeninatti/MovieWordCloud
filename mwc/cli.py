import click

from mwc.core.cfg import load_config
from mwc.core.db.models import init_db
from mwc.core.logger import config_logger
import logging
from mwc.bots.cli import tweet_movie
from mwc.core.movies.cli import sync_tmdb
from mwc.core.subtitles.cli import download_missing_subtitles

CONFIG = load_config()
log = logging.getLogger(__name__)


@click.group(name='mwc')
@click.pass_context
def main(ctx):
    """MovieWordCloud CLI"""
    init_db(**CONFIG['DB'])
    ctx.ensure_object(dict)
    config_logger()
    log.info("Init the main application")


main.add_command(sync_tmdb)
main.add_command(download_missing_subtitles)
main.add_command(tweet_movie)

if __name__ == '__main__':
    main(obj={})
