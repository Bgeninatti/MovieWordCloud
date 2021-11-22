
import json
import re
import string

from .cfg import load_config

CONFIG = load_config()


TAG_RE = re.compile(r'(<[^>]+>)')


def tokenize_text(text):
    # Find and remove all html like tags <i>, <font>, etc
    tags = set(TAG_RE.findall(text))
    for tag in tags:
        text = text.replace(tag, '')
    # Remove punctuation and other stuff that we don't want to include
    excluded_chars = str.maketrans('', '', string.punctuation + "¡¿1234567890\\\"")
    words = text.translate(excluded_chars).strip().lower().replace('\n', ' ')
    # Remove duplicated spaces
    words = re.sub(' +', ' ', words)
    # exclude words of two characters or less
    words = ' '.join([w for w in words.split(' ') if len(w) > 2])
    return words


def get_stop_words():
    with open(CONFIG['STOP_WORDS_JSON_FILE']) as json_file:
        return json.loads(json_file.read())


def get_headers():
    return {'User-agent': 'TemporaryUserAgent v1.2'}
