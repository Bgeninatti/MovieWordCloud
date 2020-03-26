import argparse
from datetime import datetime

from mwc.cfg import DB_PATH, TWITTER_CREDENTIALS
from mwc.helpers import get_stop_words
from mwc.imdb_client import ImdbClient
from mwc.logger import get_logger
from mwc.models import Movie, get_or_create_by_imdb_movie, init_db
from mwc.opensubitles import OpenSubtitles
from mwc.twitter_bot import TwitterClient
from mwc.wordcloud import WordCloud

logger = get_logger(__name__)



parser = argparse.ArgumentParser(
    description="Search a movie in IMDB based on the provided keyword. Search the subtitle in OpenSubtitles, generates the " + \
                "wordcloud and tweets the result")
parser.add_argument('-q', '--query', dest="query", required=True,
                    help='Query to search the movie')

def main(query):
    # Search movie in IMDB
    imdb_client = ImdbClient()
    imdb_movie = imdb_client.search_movie_by_keyword(query)
    if not imdb_movie:
        logger.info("Movie not found with keyword: keyword='%s'", query)
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

    # Create wordcloud and tweet
    stop_words = get_stop_words()
    wc = WordCloud(movie, stop_words)
    wc.create()
    client = TwitterClient(**TWITTER_CREDENTIALS)
    message = f"{movie.name} ({movie.year})\n\n#MovieWordCloud"
    client.tweet_image(wc.filename, message)
    movie.last_upload = datetime.now()
    movie.save()

if __name__ == '__main__':
    args = vars(parser.parse_args())
    init_db(DB_PATH)
    main(args['query'])
    init_db(DB_PATH)
