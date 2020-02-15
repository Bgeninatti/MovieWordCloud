import os
import srt
import string
import re
import imdb
import json
from datetime import datetime
from wordcloud import WordCloud
from models import Movie, init_db, get_next_movie
from cfg import DB_PATH, STOP_WORDS_JSON_FILE, PNG_FOLDER, DEFAULT_LANGUAGE_ID

# SRT Helpers
def open_srt(srt_file):
    """
    Return a list of string
    """
    generator = srt.parse(srt.make_legal_content(srt_file.read()))
    return list(generator)

def tokenize_subtittle(subtitle):
    text = subtitle.content.replace('<i>', '').replace('</i>', '')
    excluded_chars = str.maketrans('', '', string.punctuation + "¡¿1234567890\\\"")
    words = text.translate(excluded_chars).strip().lower().replace('\n', ' ')
    words = re.sub(' +', ' ', words)
    return words

def get_stop_words():
    with open(STOP_WORDS_JSON_FILE) as json_file:
        return json.loads(json_file.read())

# Wordcloud helpers
def create_wordcloud_for_next_movie():
    init_db(DB_PATH)
    movie = get_next_movie()

    print(f"Selected movie: Name={movie.name}, LanguageId={DEFAULT_LANGUAGE_ID}")
    with open(movie.srt_file, encoding="utf-8") as srt_file:
        subtittles = open_srt(srt_file)
    words = ' '.join(map(tokenize_subtittle, subtittles))
    stop_words = get_stop_words()
    wordcloud_title = f"{movie.name} ({movie.year})"
    destination = os.path.join(PNG_FOLDER, f"{wordcloud_title}.png")
    create_wordclod(words, stop_words, destination)
    movie.last_upload = datetime.now()
    movie.save()
    return destination, wordcloud_title

def create_wordclod(words, stop_words, filename):
    cloud = WordCloud(background_color="white",
                      max_words=200,
                      stopwords=set(stop_words),
                      width=1280,
                      height=720)
    cloud.generate(words)
    cloud.to_file(filename)

def get_top250():
    ia = imdb.IMDb()
    return ia.get_top250_movies()
