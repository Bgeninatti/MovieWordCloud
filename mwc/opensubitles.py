import gzip
import os
from io import BytesIO, StringIO

import requests
import srt

from .cfg import DEFAULT_LANGUAGE_ID, SRT_FOLDER
from .helpers import get_headers
from .logger import get_logger

logger = get_logger(__name__)


class Subtitle:

    def __init__(self, subtitle_id, language, srt_file):
        self.subtitle_id = subtitle_id
        self.srt_location = os.path.join(SRT_FOLDER, f"{self.subtitle_id}.srt")
        self.language = language
        self.file = srt_file

    def get_lines(self):
        lines = srt.parse(srt.make_legal_content(self.file.read()))
        self.file.seek(0)
        return lines

    def is_valid(self):
        try:
            self.get_lines()
            return True
        except srt.SRTParseError as error:
            if "Sorry, maximum download count for IP" in str(error):
                logger.error("Error: reason='API limit reached'")
                return False
            logger.error("Error: reason='%s'", error)
            return False
        return True

    def save_srt_file(self):
        with open(self.srt_location, "w") as srtf:
            srtf.write(self.file.read())

    @classmethod
    def get_from_movie(cls, movie):
        subtitle_id = os.path.split(movie.srt_file)[-1].replace('.srt', '')
        return cls(subtitle_id, movie.language_id, open(movie.srt_file))


class OpenSubtitles:

    SEARCH_BY_IMDB_URL = 'https://rest.opensubtitles.org/search/imdbid-{imdb_id}/sublanguageid-{language_id}'

    def download_subtitle(self, sub_download_link, encoding="ISO-8859-1"):
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

    def get_valid_subtitle(self, movie, language=DEFAULT_LANGUAGE_ID):

        all_subtitles = self.search_subtitles(movie.imdb_id, language)
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
