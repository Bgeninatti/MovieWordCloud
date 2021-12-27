import click
import logging

from mwc.core.cfg import load_config

from mwc.core.db.queries import get_next_movie
from .twitter import TwitterClient
from mwc.core.wc.service import WordCloudService

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
    wc_service = WordCloudService(srt_folder)
    twitter_client = TwitterClient(**twitter_credetials)
    movie = get_next_movie()
    log.info("Selected movie: Name='%s', LanguageId='%s'", movie.original_title, language)
    wc = wc_service.build_from_movie(movie)
    twitter_client.tweet_wordcloud(movie, wc.filename, twitter_account_name)
