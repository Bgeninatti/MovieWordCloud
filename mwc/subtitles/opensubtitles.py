import gzip
from io import BytesIO, StringIO

import os
from typing import Dict, List, Optional
import requests
import json
import logging
from mwc.db.models import Movie

from .subtitle import Subtitle

log = logging.getLogger(__name__)


class OpenSubtitles:

    _SEARCH_BY_IMDB_URL = 'https://rest.opensubtitles.org/search/imdbid-{imdb_id}/sublanguageid-{language}'
    _HEADERS = {'User-agent': 'TemporaryUserAgent v1.2'}

    def __init__(self, srt_folder: str, language: str):
        """Check if the srt folder exist and create it

        Args:
            srt_folder (str): folder name without path
            language (str): language ej 'eng'
        """
        self.language = language
        if not os.path.exists(srt_folder):
            os.mkdir(srt_folder)
        self.srt_folder = srt_folder

    def download_subtitle(self, sub_download_link: str, encoding="utf-8") -> StringIO:
        """Download, extract and read the subtitle.

        Args:
            sub_download_link (str): 'https://dl.opensubtitles.org/en/download/src-api/...'
            encoding (str, optional): Defaults to "utf-8".

        Returns:
            StringIO: with the subtitle
        """
        url = sub_download_link
        response = requests.get(url)
        try:
            unziped_srt = gzip.GzipFile(fileobj=BytesIO(response.content))
            return StringIO(unziped_srt.read().decode(encoding))
        except OSError:
            return StringIO(response.content.decode(encoding))

    def search_subtitles(self, imdb_id: int) -> List[Dict]:
        """Search subtitles based on a imdb_id to return
        a list of subtitles sorted by score.

        Args:
            imdb_id (int): Id from the movie form IMDB

        Returns:
            List[Dict]: List of dictionaries that represent each
            subtitle, sorted by score
        """
        url = self._SEARCH_BY_IMDB_URL.format(imdb_id=imdb_id, language=self.language)
        response = requests.get(url, headers=self._HEADERS)
        sorted_subtitles = sorted(response.json(), key=lambda item: item['Score'])
        return sorted_subtitles

    def get_valid_subtitle(self, movie: Movie) -> Optional[Subtitle]:
        """From a IMDB movie search teh subtitles on opensubtitle.
        Get the best rakend subtitle and return a Subtitle instance
        for the DB.

        Args:
            movie (Movie): model that represent a IMDB movie

        Returns:
            Subtitle: Subtitle model instance
        """
        try:
            all_subtitles = self.search_subtitles(movie.imdb_id)
        except json.JSONDecodeError as error:
            # Sometimes opensubtitles do not return a JSON for some reason :/
            log.error("Error decoding OpenSubtitle response: reason='%s'", error)
            return

        log.info(
            "Subtitles found: imdb_id=%s, subtitles_count=%d",
            movie.imdb_id, len(all_subtitles)
        )

        subtitle = None
        for sub in all_subtitles:
            try:
                srt_file = self.download_subtitle(sub['SubDownloadLink'], "utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError) as error:
                log.error("Error: reason='%s'", error)
                continue
            subtitle = Subtitle(sub['IDSubtitleFile'], sub['SubLanguageID'], srt_file, self.srt_folder)
            if subtitle.is_valid():
                subtitle.save_srt_file()
                break

        if not subtitle:
            log.error("Error: reason='No valid subtitle found'")
            return

        return subtitle
