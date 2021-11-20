import click

from ..cfg import load_config
from ..helpers import get_stop_words
from ..logger import get_logger
from ..models import get_next_movie, init_db
from ..wordcloud import WordCloud
from .twitter import TwitterClient

logger = get_logger(__name__)
CONFIG = load_config()


@click.command()
def tweet_movie():
    """
    Tweets a random movie stored in the local database.
    """
    init_db(CONFIG['DB_PATH'])
    movie = get_next_movie()
    logger.info("Selected movie: Name='%s', LanguageId='%s'",
                movie.name, CONFIG['DEFAULT_LANGUAGE_ID'])
    stop_words = get_stop_words()
    wc = WordCloud(movie, stop_words)
    wc.to_file()
    client = TwitterClient(**CONFIG['TWITTER_CREDENTIALS'])
    client.tweet_wordcloud(movie, wc.filename)
