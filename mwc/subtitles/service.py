import logging

from mwc.db.queries import get_movies_without_subtitles
from mwc.subtitles.opensubtitles import OpenSubtitles

log = logging.getLogger(__name__)


class SubtitlesService:

    def __init__(self, srt_folder: str, language: str):
        self._subtitles = OpenSubtitles(srt_folder, language)

    def sync(self):
        movies = get_movies_without_subtitles()
        log.info("Movies with missing subtitles: movies_count=%s", len(movies))

        saved_subtitles = 0
        for movie in movies:
            subtitle = self._subtitles.get_valid_subtitle(movie)
            if subtitle is not None:
                movie.opensubtittle_id = subtitle.subtitle_id
                movie.srt_file = subtitle.srt_location
                movie.save()
                saved_subtitles += 1
        log.info("New subtitles saved: subtitles_saved=%d", saved_subtitles)
