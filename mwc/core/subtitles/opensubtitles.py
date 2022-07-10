import gzip
from io import BytesIO, StringIO

from typing import Dict, List, Iterator
import requests
import json
import logging
from mwc.core.db.models import Movie

from .subtitle import Subtitle, SubtitleError

logger = logging.getLogger('mwc')


class SubtitlesProviderError(Exception):
    ...


class OpenSubtitles:

    _search_url = 'https://rest.opensubtitles.org/search/imdbid-{imdb_id}/sublanguageid-{language}'
    _headers = {'User-agent': 'TemporaryUserAgent v1.2'}

    @staticmethod
    def _download_content(url: str, encoding="utf-8") -> str:
        """Download, extract and read the subtitle.

        Args:
            url (str): 'https://dl.opensubtitles.org/en/download/src-api/...'
            encoding (str, optional): Defaults to "utf-8".

        Returns:
            StringIO: with the subtitle
        """
        url = url
        response = requests.get(url)
        try:
            unziped_srt = gzip.GzipFile(fileobj=BytesIO(response.content))
            return unziped_srt.read().decode(encoding)
        except OSError:
            return response.content.decode(encoding)

    def _search_subtitles(self, imdb_id: int, language: str) -> List[Dict]:
        """Search subtitles based on a imdb_id to return
        a list of subtitles sorted by score.

        Args:
            imdb_id (int): IMDBId
            language (str): language code

        Returns:
            List[Dict]: List of dictionaries that represent each
            subtitle, sorted by score
        """
        sorted_subtitles = []
        try:
            url = self._search_url.format(imdb_id=imdb_id, language=language)
            response = requests.get(url, headers=self._headers)
            sorted_subtitles = sorted(response.json(), key=lambda item: item['Score'])
        except json.JSONDecodeError as error:
            # Sometimes opensubtitles do not return a JSON :/
            logger.debug('Error searching subtitles', extra={'imdb_id':  imdb_id, 'reason': error})
            pass
        return sorted_subtitles

    def get_subtitles(self, movie: Movie, language: str = None) -> Iterator[Subtitle]:
        """From a IMDB movie search teh subtitles on opensubtitle.
        Get the best rakend subtitle and return a Subtitle instance
        for the DB.

        Args:
            movie (Movie): model that represent a IMDB movie
            movie (str): Desired subtitle language

        Returns:
            Subtitle: Subtitle model instance
        """
        language = language or movie.original_language
        subtitles_data = self._search_subtitles(movie.imdb_id, language)
        for data in subtitles_data:
            try:
                content = self._download_content(data['SubDownloadLink'], data['SubEncoding'] or 'utf-8')
            except LookupError:
                logger.debug('Invalid encoding', extra={'imdb_id': movie.imdb_id,'encoding': data['SubEncoding']})
                continue
            except (UnicodeEncodeError, UnicodeDecodeError) as error:
                logger.debug('Decoding error', extra={'imdb_id': movie.imdb_id, 'reason': str(error)})
                continue

            try:
                subtitle = Subtitle(
                    subtitle_id=data['IDSubtitleFile'],
                    language=data['SubLanguageID'],
                    content=content,
                )
            except SubtitleError as err:
                logger.debug(str(err))
                continue
            yield subtitle
        raise StopIteration
