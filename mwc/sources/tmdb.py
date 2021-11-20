from datetime import datetime

import requests
from mwc.models import Movie


class TMDB:

    _BASE_URL = 'https://api.themoviedb.org/3'
    _GET_DETAILS_URI = '/movie/{movie_id}?api_key={api_key}'
    _GET_MOST_POPULAR_URI = '/movie/popular?api_key={api_key}&page={page}'

    def __init__(self, api_key):
        self._api_key = api_key

    def _get(self, uri):
        url = f"{self._BASE_URL}{uri}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_movie(self, movie_id: int):
        uri = self._GET_DETAILS_URI.format(api_key=self._api_key, movie_id=movie_id)
        data = self._get(uri)
        if not data['imdb_id']:
            return
        return Movie(
            budget=data['budget'],
            tmdb_id=data['id'],
            imdb_id=data['imdb_id'],
            original_language=data['original_language'],
            original_title=data['original_title'],
            popularity=data['popularity'],
            poster_path=data['poster_path'],
            release_date=datetime.strptime(data['release_date'], "%Y-%m-%d"),
            revenue=data['revenue'],
            runtime=data['runtime'],
        )

    def get_most_popular(self, page=1):
        uri = self._GET_MOST_POPULAR_URI.format(api_key=self._api_key, page=page)
        data = self._get(uri)
        for movie in data['results']:
            yield movie['id']
