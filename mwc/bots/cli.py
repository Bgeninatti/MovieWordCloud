import click
import logging

from mwc.cfg import load_config

from mwc.helpers import get_stop_words
from ..db.queries import get_next_movie
from mwc.wordcloud import WordCloud
from .twitter import TwitterClient

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
@click.argument('srt_folder', type=str, default=CONFIG['SRT_FOLDER'])
@click.argument('language', type=str, default=CONFIG['DEFAULT_LANGUAGE_ID'])
@click.argument('twitter_credetials', type=dict, default=CONFIG['TWITTER_CREDENTIALS'])
@click.argument('twitter_account_name', type=str, default=CONFIG['TWITTER_ACCOUNT_NAME'])
def tweet_movie(srt_folder, language, twitter_credetials, twitter_account_name):
    """
    Tweets a random movie stored in the local database.
    """
    movie = get_next_movie()
    log.info("Selected movie: Name='%s', LanguageId='%s'", movie.original_title, language)
    stop_words = get_stop_words()
    wc = WordCloud(movie, stop_words, srt_folder)
    wc.to_file()
    client = TwitterClient(**twitter_credetials)
    client.tweet_wordcloud(movie, wc.filename, twitter_account_name)
