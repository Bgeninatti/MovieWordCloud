import srt
import requests
import gzip
from io import StringIO, BytesIO


class AuthException(Exception):
    pass


class OpenSubtitles:

    LOGIN_URL = 'https://rest.opensubtitles.org/auth'
    SUBTITLES_URL = 'http://dl.opensubtitles.org/en/download/src-api/vrf-19d50c5e/sid-{token}/filead/{subtitle_id}.srt'
    SEARCH_BY_IMDB_URL = 'https://rest.opensubtitles.org/search/imdbid-{imdb_id}/sublanguageid-{language_id}'

    def __init__(self, user, password):
        self._token = self._login(user, password)

    def _get_headers(self):
        return {'User-agent': 'TemporaryUserAgent v1.2'}

    def _login(self, user, password):
        data = {'username': user, 'password': password}
        headers = self._get_headers()
        response = requests.post(self.LOGIN_URL, data, headers=headers)
        auth = response.json()
        if auth['success']:
            return auth['session_id']
        raise AuthException(response.text)

    def download_subtitle(self, sub_download_link, encoding="ISO-8859-1"):
        # url = self.SUBTITLES_URL.format(token=self._token, subtitle_id=subtitle_id)
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
