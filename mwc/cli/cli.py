import click

from mwc.core.cfg import settings
from mwc.core.db.models import init_db
from mwc.core.logger import setup_logger
from mwc.cli.commands import tweet_movie, sync_subtitles, sync_movies, sync_stopwords


@click.group(name='mwc')
def main():
    """MovieWordCloud CLI"""
    init_db(**settings['DB'])
    setup_logger()


main.add_command(sync_stopwords)
main.add_command(sync_movies)
main.add_command(sync_subtitles)
main.add_command(tweet_movie)


if __name__ == '__main__':
    main(obj={})
