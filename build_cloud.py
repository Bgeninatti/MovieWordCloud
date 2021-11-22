
import argparse
import logging
from mwc.cfg import DB_PATH
from mwc.helpers import get_stop_words
from mwc.imdb_client import ImdbClient

from mwc.models import get_or_create_by_imdb_movie, init_db
from mwc.opensubitles import OpenSubtitles
from mwc.wordcloud import WordCloud


log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Search a movie in IMDB based on the provided keyword. Search the subtitle in " + \
    "OpenSubtitles, generates the wordcloud witouth tweeting the result")
parser.add_argument('-q', '--query', dest="query", required=True,
                    help='Query to search the movie')


def search_and_build(query):
    # Search movie in IMDB
    imdb_client = ImdbClient()
    imdb_movie = imdb_client.search_movie_by_keyword(query)
    if not imdb_movie:
        log.info("Movie not found with keyword: keyword='%s'", query)
        return
    movie = get_or_create_by_imdb_movie(imdb_movie)

    # Download Subtitle
    os_client = OpenSubtitles()
    subtitle = os_client.get_valid_subtitle(movie)
    if subtitle:
        movie.opensubtittle_id = subtitle.subtitle_id
        movie.language_id = subtitle.language
        movie.srt_file = subtitle.srt_location
        movie.save()
    else:
        return
    stop_words = get_stop_words()
    wc = WordCloud(movie, stop_words)
    wc.to_file()


if __name__ == '__main__':
    args = vars(parser.parse_args())
    init_db(DB_PATH)
    search_and_build(args['query'])
