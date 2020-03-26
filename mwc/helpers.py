
import json
import re
import string

from .cfg import STOP_WORDS_JSON_FILE


def tokenize_text(text):
    excluded_chars = str.maketrans('', '', string.punctuation + "¡¿1234567890\\\"")
    words = text.translate(excluded_chars).strip().lower().replace('\n', ' ')
    words = re.sub(' +', ' ', words)
    return words

def get_stop_words():
    with open(STOP_WORDS_JSON_FILE) as json_file:
        return json.loads(json_file.read())

def get_headers():
    return {'User-agent': 'TemporaryUserAgent v1.2'}
