
import os

def load_config():
    config = {
        'SRT_FOLDER': os.environ['SRT_FOLDER'],
        'PNG_FOLDER': os.environ['PNG_FOLDER'],
        'DEFAULT_LANGUAGE_ID': os.environ['DEFAULT_LANGUAGE_ID'],
        'DB_PATH': os.environ['DB_PATH'],
        'STOP_WORDS_JSON_FILE': os.environ['STOP_WORDS_JSON_FILE'],
        'TWITTER_CREDENTIALS': {
            'consumer_key': os.environ['TWITTER_CONSUMER_KEY'],
            'consumer_secret': os.environ['TWITTER_CONSUMER_SECRET'],
            'access_token': os.environ['TWITTER_ACCESS_TOKEN'],
            'access_token_secret': os.environ['TWITTER_ACCESS_TOKEN_SECRET']
        },
        'TWITTER_ACCOUNT_NAME': os.environ['TWITTER_ACCOUNT_NAME'],
        'TMDB_API_KEY': os.environ['TMDB_API_KEY']
    }

    return config