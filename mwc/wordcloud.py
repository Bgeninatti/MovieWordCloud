import os

from wordcloud import WordCloud as WC

from .cfg import PNG_FOLDER
from .helpers import tokenize_text
from .subtitles.subtitle import Subtitle


class WordCloud:

    def __init__(self, movie, stop_words):
        self.movie = movie
        self.stop_words = stop_words
        self.subtitle = Subtitle.get_from_movie(movie)
        lines = [l.content for l in self.subtitle.get_lines()]
        self.words = tokenize_text(' '.join(lines))
        self.wordcloud_title = f"{self.movie.name} ({self.movie.year})"
        self.filename = os.path.join(PNG_FOLDER, f"{self.wordcloud_title}.png")
        self.cloud = WC(background_color="white",
                        max_words=200,
                        stopwords=set(self.stop_words),
                        width=1280,
                        height=720,
                        collocations=False) # Related to issue_5: Duplicated words in word cloud.
                                            # With this parameter in False we avoid repeated words.
        self.cloud.generate(self.words)

    def to_file(self):
        self.cloud.to_file(self.filename)

