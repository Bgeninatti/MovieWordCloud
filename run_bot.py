

from datetime import datetime

from mwc.cfg import (DB_PATH, DEFAULT_LANGUAGE_ID, TWITTER_ACCOUNT_NAME,
                     TWITTER_CREDENTIALS)
from mwc.helpers import get_stop_words
from mwc.logger import get_logger
from mwc.models import get_next_movie, init_db
from mwc.twitter_bot import TwitterClient
from mwc.wordcloud import WordCloud

logger = get_logger(__name__)


def tweet_movie_wordcloud():
    init_db(DB_PATH)
    movie = get_next_movie()
    logger.info("Selected movie: Name='%s', LanguageId='%s'", movie.name, DEFAULT_LANGUAGE_ID)
    stop_words = get_stop_words()
    wc = WordCloud(movie, stop_words)
    wc.to_file()
    client = TwitterClient(**TWITTER_CREDENTIALS)
    client.tweet_wordcloud(movie, wc.filename)
    movie.last_upload = datetime.now()
    movie.save()

if __name__ == '__main__':
    tweet_movie_wordcloud()

