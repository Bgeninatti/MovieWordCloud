import click
from mwc.logger import config_logger
import logging
from mwc.bots.cli import tweet_movie
from mwc.sources.cli import sync_imdb
from mwc.subtitles.cli import download_missing_subtitles


log = logging.getLogger(__name__)


@click.group(name='mwc')
@click.pass_context
def main(ctx):
    #TODO: Inicializar la db aca y no en cada comando
    """MovieWordCloud CLI"""
    ctx.ensure_object(dict)
    config_logger()
    log.info("Init the main application")


main.add_command(sync_imdb)
main.add_command(download_missing_subtitles)
main.add_command(tweet_movie)

if __name__ == '__main__':
    main(obj={})

