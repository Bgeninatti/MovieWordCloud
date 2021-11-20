from datetime import datetime

import tweepy

from ..cfg import load_config

CONFIG = load_config()


class TwitterClient:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_image(self, filename, message):
        return self.api.update_status_with_media(status=message, filename=filename)

    def answer_tweet(self, text, tweet_id):
        return self.api.update_status(status=text, in_reply_to_status_id=tweet_id)

    def tweet_wordcloud(self, movie, wc_filename):
        message = f"{movie.name} ({movie.year})\n\n#MovieWordCloud"
        answer_tweet = f"{CONFIG['TWITTER_ACCOUNT_NAME']}\n\n https://www.imdb.com/title/tt{movie.imdb_id}"
        image_tweet = self.tweet_image(wc_filename, message)
        self.answer_tweet(answer_tweet, image_tweet.id)
        movie.last_upload = datetime.now()
        movie.save()
