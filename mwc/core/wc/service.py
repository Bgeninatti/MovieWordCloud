from typing import List

from mwc.core.db.models import Movie
from mwc.core.storage import get_storage
from mwc.core.subtitles.service import SubtitlesService
from wordcloud import WordCloud as WC
from mwc.core.wc.stop_words import StopWordsService


class WordCloudService:

    _stopwords_service = StopWordsService()
    _subtitle_service = SubtitlesService()

    def build_from_movie(self, movie: Movie):
        subtitle = self._subtitle_service.get_from_movie(movie)
        stop_words = self._stopwords_service.get(movie.original_language)
        wc = self.build(subtitle.get_words(), stop_words)
        return wc

    def build(
        self,
        words: str,
        stop_words: List[str],
        background_color='white',
        max_words=200,
        width=1280,
        height=720,
    ):
        # collocations=False avoids repeated words (issue#5)
        cloud = WC(
            background_color=background_color,
            max_words=max_words,
            stopwords=set(stop_words),
            width=width,
            height=height,
            collocations=False
        )

        cloud.generate(words)
        return cloud
