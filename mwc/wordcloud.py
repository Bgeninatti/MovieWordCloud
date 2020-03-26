import os

from wordcloud import WordCloud as WC

from .cfg import PNG_FOLDER
from .helpers import tokenize_text
from .opensubitles import Subtitle


class WordCloud:

    def __init__(self, movie, stop_words):
        self.movie = movie
        self.stop_words = stop_words
        self.subtitle = Subtitle.get_from_movie(movie)
        lines = [l.content for l in self.subtitle.get_lines()]
        self.words = ' '.join(map(tokenize_text, lines))
        self.wordcloud_title = f"{self.movie.name} ({self.movie.year})"
        self.filename = os.path.join(PNG_FOLDER, f"{self.wordcloud_title}.png")

    def create(self):
        cloud = WC(background_color="white",
                   max_words=200,
                   stopwords=set(self.stop_words),
                   width=1280,
                   height=720,
                   collocations=False) # Related to issue_5: Duplicated words in word cloud.
                                       # With this parameter in False we avoid repeated words.
        cloud.generate(self.words)
        cloud.to_file(self.filename)

