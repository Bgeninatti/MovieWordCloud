import logging

from mwc.core.db.queries import get_existing_tmdb_ids
from mwc.core.movies.tmdb import TmdbClient

log = logging.getLogger(__name__)


class MoviesService:

    def __init__(self, tmdb_api_key: str, fetch_ranking_pages: int = 1):
        self._tmdb = TmdbClient(tmdb_api_key)
        self.fetch_ranking_pages = fetch_ranking_pages

    def sync(self):
        tmdb_ids = get_existing_tmdb_ids()

        fetched_movies = self._tmdb.fetch(pages=self.fetch_ranking_pages)
        new_movies = {
            tmdb_id for tmdb_id in fetched_movies
            if tmdb_id not in tmdb_ids
        }

        log.info("New movies found: movies_found=%d", len(new_movies))

        saved_movies = 0
        for tmdb_id in new_movies:
            movie = self._tmdb.get_movie(tmdb_id)
            if not movie:
                log.warning("No IMDB Id found for movie: tmdb_id=%s", tmdb_id)
                continue
            movie.save()
            saved_movies += 1
        log.info("New movies saved: movies_saved=%d", saved_movies)
