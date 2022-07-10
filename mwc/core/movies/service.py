import logging

from mwc.core.db.queries import get_existing_tmdb_ids
from mwc.core.movies.tmdb import TmdbClient

logger = logging.getLogger('mwc')


class MoviesService:

    def __init__(self, tmdb_api_key: str, fetch_ranking_pages: int = 1):
        self._tmdb = TmdbClient(tmdb_api_key)
        self.fetch_ranking_pages = fetch_ranking_pages

    def sync(self):
        tmdb_ids = get_existing_tmdb_ids()
        logger.info('Fetching new movies', extra={'pages': self.fetch_ranking_pages})
        fetched_movies = self._tmdb.fetch(pages=self.fetch_ranking_pages)
        new_movies = 0
        for tmdb_id in fetched_movies:
            if tmdb_id in tmdb_ids:
                continue
            movie = self._tmdb.get_movie(tmdb_id)
            if not movie:
                logger.warning('No IMDB Id found for movie', extra={'tmdb_id': tmdb_id})
                continue
            movie.save()
            logger.info('New movie', extra={'movie': movie})
            new_movies += 1
        logger.info('New movies saved', extra={'new_movies': new_movies})
