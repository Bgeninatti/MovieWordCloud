import logging

import click

from mwc.bots.twitter import TwitterClient
from mwc.core.cfg import load_config
from mwc.core.db.queries import get_next_movie
from mwc.core.movies.service import MoviesService
from mwc.core.subtitles.service import SubtitlesService
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


@click.command()
@click.argument('srt_folder', type=str, default=CONFIG['SRT_FOLDER'])
@click.argument('language', type=str, default=CONFIG['DEFAULT_LANGUAGE_ID'])
def download_missing_subtitles(srt_folder, language):
    """
    Downloads subtitles for movies in the local database that doesn't have one yet.
    """
    service = SubtitlesService(srt_folder=srt_folder, language=language)
    service.sync()


@click.command()
@click.argument('api_key', type=str, default=CONFIG['TMDB_API_KEY'])
@click.argument('pages', type=int, default=CONFIG['FETCH_RANKING_PAGES'])
def sync_tmdb(api_key, pages):
    """
    Populates the local databse with new movies
    """
    service = MoviesService(tmdb_api_key=api_key, fetch_ranking_pages=pages)
    service.sync()
