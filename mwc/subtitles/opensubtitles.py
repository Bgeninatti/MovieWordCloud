import gzip
from io import BytesIO, StringIO

import os
import requests
import json

from mwc.cfg import load_config
from mwc.helpers import get_headers
from mwc.logger import get_logger
from .subtitle import Subtitle

logger = get_logger(__name__)
CONFIG = load_config()


class OpenSubtitles:

    SEARCH_BY_IMDB_URL = 'https://rest.opensubtitles.org/search/imdbid-{imdb_id}/sublanguageid-{language_id}'

    def __init__(self):
        if not os.path.exists(CONFIG['SRT_FOLDER']):
            os.mkdir(CONFIG['SRT_FOLDER'])

    def download_subtitle(self, sub_download_link, encoding="utf-8"):
        url = sub_download_link
        response = requests.get(url)
        try:
            unziped_srt = gzip.GzipFile(fileobj=BytesIO(response.content))
            return StringIO(unziped_srt.read().decode(encoding))
        except OSError:
            return StringIO(response.content.decode(encoding))

    def search_subtitles(self, imdb_id, language_id):
        url = self.SEARCH_BY_IMDB_URL.format(imdb_id=imdb_id, language_id=language_id)
        headers = get_headers()
        response = requests.get(url, headers=headers)
        sorted_subtitles = sorted(response.json(), key=lambda item: item['Score'])
        return sorted_subtitles

    def get_valid_subtitle(self, movie, language=CONFIG['DEFAULT_LANGUAGE_ID']):
        try:
            all_subtitles = self.search_subtitles(movie.imdb_id, language)
        except json.JSONDecodeError as error:
            # Sometimes opensubtitles do not return a JSON for some reason :/
            logger.error("Error decoding OpenSubtitle response: reason='%s'", error)
            return

        logger.info(
            "Subtitles found: imdb_id=%s, subtitles_count=%d",
            movie.imdb_id, len(all_subtitles)
        )

        subtitle = None
        for sub in all_subtitles:
            try:
                srt_file = self.download_subtitle(sub['SubDownloadLink'], "utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError) as error:
                logger.error("Error: reason='%s'", error)
                continue
            subtitle = Subtitle(sub['IDSubtitleFile'], sub['SubLanguageID'], srt_file)
            if subtitle.is_valid():
                subtitle.save_srt_file()
                break

        if not subtitle:
            logger.error("Error: reason='No valid subtitle found'")
            return
        logger.info("Download succeded")

        return subtitle
