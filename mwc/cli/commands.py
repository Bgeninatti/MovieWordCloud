import logging
from datetime import datetime
from io import BytesIO

import click

from mwc.bots.twitter import TwitterService
from mwc.core.db.queries import get_next_movie
from mwc.core.movies.service import MoviesService
from mwc.core.subtitles.service import SubtitlesService
from mwc.core.wc.service import WordCloudService
from mwc.core.wc.stop_words import StopWordsService
from mwc.core.cfg import settings


logger = logging.getLogger('mwc')


@click.command()
def tweet_movie():
    """
    Tweets a random movie stored in the local database.
    """
    wordcloud_service = WordCloudService()
    twitter_client = TwitterService(**settings['TWITTER_CREDENTIALS'])

    movie = get_next_movie()
    logger.info('Selected movie', extra={'movie': movie})
    message = f"{movie.original_title} ({movie.release_date})\n\n#MovieWordCloud"
    wordcloud = wordcloud_service.build_from_movie(movie)
    image_tweet = twitter_client.tweet_image(
        BytesIO(wordcloud.to_image().tobytes()),
        f'{movie.tmdb_id}.png',
        message,
    )
    logger.info('Wordcloud tweeted', extra={'tweet_id': image_tweet.id})
    answer_message = f"https://www.themoviedb.org/movie/{movie.tmdb_id}"
    answer_tweet = twitter_client.answer_tweet(answer_message, image_tweet.id)
    logger.info('Answer tweeted', extra={'tweet_id': answer_tweet.id})
    movie.last_tweet = datetime.now()
    movie.save()


@click.command()
def sync_subtitles():
    """
    Downloads subtitles for movies in the local database that doesn't have one yet.
    """
    service = SubtitlesService()
    service.sync()


@click.command()
def sync_movies():
    """
    Populates the local databse with new movies
    """
    service = MoviesService(
        tmdb_api_key=settings['TMDB_API_KEY'],
        fetch_ranking_pages=settings['FETCH_RANKING_PAGES'],
    )
    service.sync()


@click.command()
def sync_stopwords():
    """
    Generate stopwords for all the available languages
    """
    stopwords_service = StopWordsService()
    stopwords_service.sync()
