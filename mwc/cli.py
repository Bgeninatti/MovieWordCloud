import click

from mwc.bots.cli import tweet_movie
from mwc.sources.cli import sync_imdb
from mwc.subtitles.cli import download_missing_subtitles


@click.group(name='mwc')
@click.pass_context
def main(ctx):
    """MovieWordCloud CLI"""
    ctx.ensure_object(dict)

main.add_command(sync_imdb)
main.add_command(download_missing_subtitles)
main.add_command(tweet_movie)

if __name__ == '__main__':
    main(obj={})
