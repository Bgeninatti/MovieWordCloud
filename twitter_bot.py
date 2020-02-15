import tweepy
from cfg import TWITTER_CREDENTIALS
from helpers import create_wordcloud_for_next_movie

class TwitterClient:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_image(self, filename, message):
        self.api.update_with_media(filename, status=message)


def run_bot():
    client = TwitterClient(**TWITTER_CREDENTIALS)
    filename, message = create_wordcloud_for_next_movie()
    client.tweet_image(filename, message)

if __name__ == '__main__':
    run_bot()


