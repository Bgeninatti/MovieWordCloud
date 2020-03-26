

from lib.cfg import DB_PATH
from lib.logger import get_logger
from lib.models import Movie, init_db
from lib.opensubitles import OpenSubtitles

logger = get_logger(__name__)


def download_subtitles():
    init_db(DB_PATH)
    movies = Movie.select().where(Movie.opensubtittle_id.is_null())
    os_client = OpenSubtitles()
    logger.info("Movies with missing subtitles: movies_count=%s", len(movies))

    for movie in movies:
        subtitle = os_client.get_valid_subtitle(movie.imdb_id)
        if subtitle is not None:
            movie.opensubtittle_id = subtitle.metadata['IDSubtitleFile']
            movie.language_id = subtitle.metadata['SubLanguageID']
            movie.srt_file = subtitle.srt_location
            movie.save()

if __name__ == '__main__':
    download_subtitles()
