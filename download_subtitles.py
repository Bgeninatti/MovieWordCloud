
import os
import srt
from helpers import open_srt
from cfg import SRT_FOLDER, DEFAULT_LANGUAGE_ID, DB_PATH
from models import Movie, init_db
from opensubitles import OpenSubtitles
from logger import get_logger

logger = get_logger(__name__)


def download_subtitles():
    init_db(DB_PATH)
    movies = Movie.select().where(Movie.opensubtittle_id.is_null())
    os_client = OpenSubtitles()
    logger.info("Movies with missing subtitles: movies_count=%s", len(movies))

    for movie in movies:
        all_subtitles = os_client.search_subtitles(movie.imdb_id, DEFAULT_LANGUAGE_ID)
        logger.info("Subtitles found: imdb_id=%s, subtitles_count=%d", movie.imdb_id, len(all_subtitles))

        is_valid_subtitle = False
        while not is_valid_subtitle:
            try:
                sub = all_subtitles.pop()
                logger.info("Attempt to download subtitle: subtitle_id=%s", sub['IDSubtitleFile'])
                srt_filename = os.path.join(SRT_FOLDER, f"{sub['IDSubtitleFile']}.srt")
                srt_file = os_client.download_subtitle(sub['SubDownloadLink'], "utf-8")
                open_srt(srt_file) # Just to validate the srt encoding
                srt_file.seek(0)
                with open(srt_filename, "w") as srtf:
                    srtf.write(srt_file.read())
                is_valid_subtitle = True
                logger.info(f"Download succeded")
            except srt.SRTParseError as error:
                if "Sorry, maximum download count for IP" in str(error):
                    logger.error("Error: reason='API LIMIT REACHED!'")
                    return
                logger.error("Error: reason='%s'", error)
                continue
            except (UnicodeEncodeError, UnicodeDecodeError) as error:
                logger.error("Error: reason='%s'", error)
                continue
            except IndexError as error:
                logger.error("Error: reason='No valid subtitle found'")
                sub = None
                break

        if sub is not None:
            movie.opensubtittle_id = sub['IDSubtitleFile']
            movie.language_id = DEFAULT_LANGUAGE_ID
            movie.srt_file = srt_filename
            movie.save()

if __name__ == '__main__':
    download_subtitles()
