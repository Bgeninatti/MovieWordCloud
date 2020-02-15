import os
import wordcloud
import nltk
import srt
import string
import re
import imdb
import random
import json
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from cfg import OPENSUBTITTLES_USER, OPENSUBTITTLES_PASS, STOP_WORDS_JSON_FILE

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
