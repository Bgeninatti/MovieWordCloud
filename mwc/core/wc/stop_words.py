import json
import logging
from collections import Counter
from io import StringIO
from itertools import chain

from mwc.core.db.queries import get_movies_with_subtitles, get_movies_languages
from mwc.core.storage import get_storage
from mwc.core.subtitles.service import SubtitlesService


logger = logging.getLogger('mwc')


class StopWordsService:

    _storage = get_storage(namespace='stopwords')
    _subtitles_service = SubtitlesService()

    def calculate(self, language: str, threshold: float = 0.3):
        movies = get_movies_with_subtitles(language)
        if not movies:
            logger.warning('No movies with subtitles found', extra={'language': language})
            return
        subtitles = [
            self._subtitles_service.get_from_movie(movie)
            for movie in movies
        ]
        words = chain(*[subtitle.get_words() for subtitle in subtitles])
        counter = dict(Counter(words))
        occurrences_threshold = max(counter.values()) * threshold
        stop_words = []
        for word, occurrences in counter.items():
            if occurrences >= occurrences_threshold:
                stop_words.append(word)
            continue

        filename = f'{language}.json'
        stopword_file = StringIO(json.dumps(stop_words))
        self._storage.save(filename, stopword_file)
        logger.info(
            'Stopwords calculated',
            extra={
                'stopwords': len(stop_words),
                'language': language,
                'occurrences_threshold': occurrences_threshold,
                'threshold': threshold,
            }
        )

    def get(self, language: str):
        stopwords_file = self._storage.get(f'{language}.json')
        if stopwords_file is None:
            raise FileNotFoundError(
                f'No stop words found: language={language}'
            )
        return stopwords_file.json()

    def sync(self, threshold: float = 0.3):
        languages = get_movies_languages()
        for language in languages:
            self.calculate(language, threshold)
