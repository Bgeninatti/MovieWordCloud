
import click,logging

from mwc.cfg import load_config

from mwc.models import Movie

from .opensubtitles import OpenSubtitles

log = logging.getLogger(__name__)
CONFIG = load_config()


@click.command()
def download_missing_subtitles():
    """
    Downloads subtitles for movies in the local database that doesn't have one yet.
    """
    movies = Movie.select().where(Movie.opensubtittle_id.is_null())
    os_client = OpenSubtitles()
    log.info("Movies with missing subtitles: movies_count=%s", len(movies))

    for movie in movies:
        subtitle = os_client.get_valid_subtitle(movie)
        if subtitle:
            movie.opensubtittle_id = subtitle.subtitle_id
            movie.language_id = subtitle.language
            movie.srt_file = subtitle.srt_location
            movie.save()
