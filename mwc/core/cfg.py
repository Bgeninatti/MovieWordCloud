
import os
from urllib.parse import urlparse


def load_settings():
    params = urlparse(os.environ["DATABASE_URL"])
    config = {
        'FETCH_RANKING_PAGES': int(clean_setting('FETCH_RANKING_PAGES')),
        'DB': {
            'db_name': params.path[1:],
            'user': params.username,
            'password': params.password,
            'host': params.hostname,
            'port': params.port,
        },
        'TWITTER_CREDENTIALS': {
            'consumer_key': clean_setting('TWITTER_CONSUMER_KEY'),
            'consumer_secret': clean_setting('TWITTER_CONSUMER_SECRET'),
            'access_token': clean_setting('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': clean_setting('TWITTER_ACCESS_TOKEN_SECRET')
        },
        'TMDB_API_KEY': clean_setting('TMDB_API_KEY'),
        'DROPBOX_TOKEN': clean_setting('DROPBOX_TOKEN'),

    }

    return config


def clean_setting(key):
    return os.environ[key].replace('\n', '').replace('\r', '')


settings = load_settings()
