from mwc.core.db.models import Movie
from mwc.core.helpers import get_stop_words
from mwc.core.wc.wordcloud import WordCloud


class WordCloudService:

    def __init__(self, srt_folder: str):
        self._stop_words = get_stop_words()
        self._srt_folder = srt_folder

    def build_from_movie(self, movie: Movie):
        wc = WordCloud(movie, self._stop_words, self._srt_folder)
        wc.to_file()
        return wc
