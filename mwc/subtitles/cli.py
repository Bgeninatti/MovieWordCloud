
import click

from ..cfg import load_config
from ..logger import get_logger
from ..models import Movie, init_db
from .opensubtitles import OpenSubtitles

logger = get_logger(__name__)
CONFIG = load_config()


@click.command()
def download_missing_subtitles():
    """
    Downloads subtitles for movies in the local database that doesn't have one yet.
    """
    init_db(CONFIG['DB_PATH'])
    movies = Movie.select().where(Movie.opensubtittle_id.is_null())
    os_client = OpenSubtitles()
    logger.info("Movies with missing subtitles: movies_count=%s", len(movies))

    for movie in movies:
        subtitle = os_client.get_valid_subtitle(movie)
        if subtitle:
            movie.opensubtittle_id = subtitle.subtitle_id
            movie.language_id = subtitle.language
            movie.srt_file = subtitle.srt_location
            movie.save()
