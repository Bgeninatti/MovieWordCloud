from io import StringIO, BytesIO

import tweepy


class TwitterService:

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> None:
        """Login into the Twiter API with tweepy
        https://docs.tweepy.org/en/stable/auth_tutorial.html

        Args:
            consumer_key (str): given when you create a new twitter application
            consumer_secret (str): given when you create a new twitter application
            access_token (str): is the token given to interact with the Twitter API
            access_token_secret (str): is the token given to interact with the Twitter API
        """
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet_image(self, image: BytesIO, filename:str, message: str = '') -> tweepy.models.Status:
        """Update the status with the image

        Args:
            file (StringIO):
            message (str): message to publish in the twitt

        Returns:
            tweepy.models.Status: Status object, simil response, with the information that
            twitter the API returns.
        """
        return self.api.media_upload(status=message, filename=filename, file=image)

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
