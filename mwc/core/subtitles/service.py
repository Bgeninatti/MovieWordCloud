import logging
from io import BytesIO

from mwc.core.db.queries import get_movies_without_subtitles
from mwc.core.storage import get_storage
from mwc.core.subtitles.opensubtitles import OpenSubtitles
from mwc.core.subtitles.subtitle import Subtitle

logger = logging.getLogger('mwc')


class SubtitlesService:

    _storage = get_storage(namespace='subtitles')
    _provider = OpenSubtitles()

    def sync(self):
        movies = get_movies_without_subtitles()
        logger.info('Movies with missing subtitles', extra={'movies_count': len(movies)})

        new_subtitles = 0
        for movie in movies:
            try:
                # Get the first valid subtitle
                subtitle = next(self._provider.get_subtitles(movie))
            except RuntimeError:
                logger.warning('No subtitles found', extra={'movie': movie})
                continue
            self._storage.save(subtitle.filename, BytesIO(subtitle.content.encode()))
            movie.subtitle_id = subtitle.subtitle_id
            movie.save()
            new_subtitles += 1
            logger.info('Subtitle found', extra={'movie': movie})
        logger.info('New subtitles saved', extra={'new_subtitles': new_subtitles})

    def get_from_movie(self, movie):
        filename = Subtitle.build_filename(movie.subtitle_id)
        content = self._storage.get(filename)
        return Subtitle(movie.subtitle_id, movie.original_language, content.text)
