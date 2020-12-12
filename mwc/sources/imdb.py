import re
from io import StringIO

import requests

import imdb
from lxml import etree

from ..logger import get_logger
from ..helpers import get_headers, tokenize_text


logger = get_logger(__name__)


class ImdbClient:


    MOST_POPULARS_MOVIES_URL = 'https://www.imdb.com/chart/moviemeter/?sort=rk,asc'
    IMDB_IDS_XPATH = '//tbody[contains(@class, "lister-list")]/tr/td[2]/a/@href'
    SEARCH_URL = 'https://v2.sg.media-imdb.com/suggestion/{first_letter}/{query}.json'

    def __init__(self):
        self._client = imdb.IMDb()

    def get_top250(self, exclude_ids=()):
        top_movies = self._client.get_top250_movies()
        movies = [m for m in top_movies if m.movieID not in exclude_ids]
        logger.info("New movies found in top 250: new_movies=%d, excluded_movies=%d",
                    len(movies),
                    len([m for m in top_movies if m.movieID in exclude_ids]))
        return movies


    def get_most_popular_movies(self, exclude_ids=()):
        htmlparser = etree.HTMLParser()
        response = requests.get(self.MOST_POPULARS_MOVIES_URL)
        result_tree = etree.parse(StringIO(response.text), htmlparser)
        hrefs = result_tree.xpath(self.IMDB_IDS_XPATH)
        movies_ids = list(map(lambda x: re.findall(r'\d+', x).pop(), hrefs))

        ids_to_download = [m for m in movies_ids if m not in exclude_ids]
        logger.info("New movies found in most populars: " + \
                    "new_movies=%d, excluded_movies=%d",
                    len(ids_to_download),
                    len([m for m in movies_ids if m in exclude_ids]))
        # TODO: This can be async
        movies = [self._client.get_movie(m_id) for m_id in ids_to_download]
        return tuple(movies)

    def search_movie_by_keyword(self, keyword):
        query = tokenize_text(keyword).replace('  ', '_')
        first_letter = query[0]
        url = self.SEARCH_URL.format(first_letter=first_letter, query=query)
        r = requests.get(url, headers=get_headers())
        data = r.json()
        if 'd' not in data.keys():
            return
        return self._client.get_movie(data['d'][0]['id'].replace('tt', ''))
