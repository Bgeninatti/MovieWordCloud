from datetime import datetime

import requests
from mwc.core.db.models import Movie


class TmdbClient:

    _BASE_URL = 'https://api.themoviedb.org/3'
    _GET_DETAILS_URI = '/movie/{movie_id}?api_key={api_key}'
    _GET_MOST_POPULAR_URI = '/movie/popular?api_key={api_key}&page={page}'
    _GET_TOP_RATED_URI = '/movie/top_rated?api_key={api_key}&page={page}'

    def __init__(self, api_key):
        self._api_key = api_key

    def _get(self, uri):
        url = f"{self._BASE_URL}{uri}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _fetch_ranking_ids(self, ranking_uri: str, pages: int = 1):
        for page in range(1, pages + 1):
            uri = ranking_uri.format(api_key=self._api_key, page=page)
            data = self._get(uri)
            for movie in data['results']:
                yield movie['id']

    def get_movie(self, movie_id: int):
        uri = self._GET_DETAILS_URI.format(api_key=self._api_key, movie_id=movie_id)
        data = self._get(uri)
        if not data['imdb_id']:
            return
        release_date = datetime.strptime(data['release_date'], "%Y-%m-%d") if data['release_date'] else None
        return Movie(
            budget=round(data['budget'] / 1000),
            tmdb_id=data['id'],
            imdb_id=data['imdb_id'],
            original_language=data['original_language'],
            original_title=data['original_title'],
            popularity=data['popularity'],
            poster_path=data['poster_path'],
            release_date=release_date,
            revenue=round(data['revenue'] / 1000),
            runtime=data['runtime'],
        )

    def fetch(self, pages: int = 1):
        yield from self._fetch_ranking_ids(self._GET_MOST_POPULAR_URI, pages)
        yield from self._fetch_ranking_ids(self._GET_TOP_RATED_URI, pages)
