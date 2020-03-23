import srt
import requests
import gzip
from io import StringIO, BytesIO


class OpenSubtitles:

    SEARCH_BY_IMDB_URL = 'https://rest.opensubtitles.org/search/imdbid-{imdb_id}/sublanguageid-{language_id}'

    def _get_headers(self):
        return {'User-agent': 'TemporaryUserAgent v1.2'}

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
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        sorted_subtitles = [v for v in
                            sorted(response.json(), key=lambda item: item['Score'])]
        return sorted_subtitles
