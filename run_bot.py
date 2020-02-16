from cfg import TWITTER_CREDENTIALS
from helpers import create_wordcloud_for_next_movie
from twitter_bot import TwitterClient


def tweet_movie_wordcloud():
    client = TwitterClient(**TWITTER_CREDENTIALS)
    filename, movie_title = create_wordcloud_for_next_movie()
    message = f"{movie_title}\n\n#MovieWordCloud"
    client.tweet_image(filename, message)

if __name__ == '__main__':
    tweet_movie_wordcloud()


