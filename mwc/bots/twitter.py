from datetime import datetime

import tweepy
from mwc.models import Movie


class TwitterClient:

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str) -> None:
        """Login into the Twiter API with tweepy
        https://docs.tweepy.org/en/stable/auth_tutorial.html

        Args:
            consumer_key (str): given when you create a new twitter application
            consumer_secret (str): given when you create a new twitter application
            access_token (str): is the token given to interact with the Twitter API
            access_token_secret (str): is the token given to interact with the Twitter API
        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_image(self, filename: str, message: str) -> tweepy.models.Status:
        """Update the status with the image

        Args:
            filename (str): filepath + file name .png TODO: pass the absolute path
            message (str): message to publish in the twitt

        Returns:
            tweepy.models.Status: Status object, simil response, with the information that
            twitter the API returns.
        """
        return self.api.update_status_with_media(status=message, filename=filename)

    def answer_tweet(self, text: str, tweet_id: int) -> tweepy.models.Status:
        """Update the status with new text

        Args:
            text (str): text to twit
            tweet_id (int): id of the twitt

        Returns:
            tweepy.models.Status: Status: Status object, simil response, with the information that
            twitter the API returns.
        """
        return self.api.update_status(status=text, in_reply_to_status_id=tweet_id)

    def tweet_wordcloud(self, movie: Movie, wc_filename: str, twitter_account_name: str) -> None:
        """Use the different funtions to twit an image based on a movie model.

        Args:
            movie (Movie): Movie instace from pewew that connect with SQLite
            wc_filename (str): filepath + file name .png TODO: pass the absolute path
            twitter_account_name (str): Twitter account name '@twitter_account_name'
        """
        message = f"{movie.original_title} ({movie.release_date})\n\n#MovieWordCloud"
        answer_tweet = f"{twitter_account_name}\n\n https://www.themoviedb.org/movie/{movie.tmdb_id}"
        image_tweet = self.tweet_image(wc_filename, message)
        self.answer_tweet(answer_tweet, image_tweet.id)
        movie.last_upload = datetime.now()
        movie.save()
