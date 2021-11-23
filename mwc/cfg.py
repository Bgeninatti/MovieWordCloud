
import os


def load_config():
    config = {
        'SRT_FOLDER': clean_setting('SRT_FOLDER'),
        'PNG_FOLDER': clean_setting('PNG_FOLDER'),
        'DEFAULT_LANGUAGE_ID': clean_setting('DEFAULT_LANGUAGE_ID'),
        'DB_PATH': clean_setting('DB_PATH'),
        'STOP_WORDS_JSON_FILE': clean_setting('STOP_WORDS_JSON_FILE'),
        'TWITTER_CREDENTIALS': {
            'consumer_key': clean_setting('TWITTER_CONSUMER_KEY'),
            'consumer_secret': clean_setting('TWITTER_CONSUMER_SECRET'),
            'access_token': clean_setting('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': clean_setting('TWITTER_ACCESS_TOKEN_SECRET')
        },
        'TWITTER_ACCOUNT_NAME': clean_setting('TWITTER_ACCOUNT_NAME'),
        'TMDB_API_KEY': clean_setting('TMDB_API_KEY')
    }

    return config

def clean_setting(key):
    return os.environ[key].replace('\n','').replace('\r','')
