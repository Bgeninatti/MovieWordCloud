
import click

from ..cfg import DB_PATH
from ..logger import get_logger
from ..models import Movie, init_db
from .opensubtitles import OpenSubtitles

logger = get_logger(__name__)


@click.command()
def download_missing_subtitles():
    init_db(DB_PATH)
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
