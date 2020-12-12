import argparse
import click
from datetime import datetime

from mwc.cfg import (DB_PATH, DEFAULT_LANGUAGE_ID, TWITTER_ACCOUNT_NAME,
                     TWITTER_CREDENTIALS)
from mwc.helpers import get_stop_words
from mwc.sources.imdb import ImdbClient
from mwc.logger import get_logger
from mwc.models import (Movie, get_next_movie, get_or_create_by_imdb_movie,
                        init_db)
from mwc.subtitles.opensubtitles import OpenSubtitles
from mwc.twitter_bot import TwitterClient
from mwc.wordcloud import WordCloud

logger = get_logger(__name__)


@click.group(name='walmart')
@click.pass_context
def main(ctx):
    """MovieWordCloud CLI"""
    ctx.ensure_object(dict)




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
    init_db(DB_PATH)
    imdb_client = ImdbClient()
    existing_movies = {m.imdb_id for m in Movie.select()}
    download_top_250(imdb_client, existing_movies)
    download_most_populars(imdb_client, existing_movies)
    args = vars(parser.parse_args())
    init_db(DB_PATH)
    search_and_build(args['query'])



main.add_command(upload_item)
