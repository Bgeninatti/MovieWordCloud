import requests

import imdb

from mwc.logger import get_logger
from mwc.helpers import get_headers, tokenize_text


logger = get_logger(__name__)


class ImdbClient:


    MOST_POPULARS_MOVIES_URL = 'https://www.imdb.com/chart/moviemeter/?sort=rk,asc'
    IMDB_IDS_XPATH = '//tbody[contains(@class, "lister-list")]/tr/td[2]/a/@href'
    SEARCH_URL = 'https://v2.sg.media-imdb.com/suggestion/{first_letter}/{query}.json'

    def __init__(self):
        self._client = imdb.IMDb()

    def get_movie(self, imdb_id):
        logger.debug("Downloading movie: imdb_id=%s", imdb_id)
        movie = self._client.get_movie(imdb_id)
        return movie

    def get_top250(self):
        logger.info("Searchig top 250 movies in imdb")
        movies = self._client.get_top250_movies()
        logger.info("Movies found in top 250: movies_count=%d", len(movies))
        return movies

    def search_movie_by_keyword(self, keyword):
        logger.info("Searchig movie: keyword=%s", keyword)
        query = tokenize_text(keyword).replace('  ', '_')
        first_letter = query[0]
        url = self.SEARCH_URL.format(first_letter=first_letter, query=query)
        r = requests.get(url, headers=get_headers())
        data = r.json()
        if 'd' not in data.keys():
            logger.info("Movie not found: keyword=%s", keyword)
            return
        movie = self._client.get_movie(data['d'][0]['id'].replace('tt', ''))
        logger.info("Movie found: movie=%s", movie)
        return movie
