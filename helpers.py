import os
import wordcloud
import nltk
import srt
import string
import re
import imdb
import random
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from pythonopensubtitles.opensubtitles import OpenSubtitles
from cfg import OPENSUBTITTLES_USER, OPENSUBTITTLES_PASS

# SRT Helpers
def open_srt(srt_file):
    """
    Return a list of string
    """
    generator = srt.parse(srt_file.read())
    return [g for g in generator]

def tokenize_subtittle(subtittle):
    excluded_chars = str.maketrans('', '', string.punctuation + "¡¿\1234567890")
    words = subtittle.content.translate(excluded_chars).strip().lower().replace('\n', ' ')
    words = re.sub(' +', ' ', words)
    return words

def get_most_common_words(words, n=10):
   wordcount = Counter([w for w in words.split(' ') if len(w) > 1])
   ranking = {k: v for k, v in sorted(wordcount.items(), key=lambda item: item[1])}
   return list(ranking.keys())[-n:] 
    
# Wordcloud helpers
def create_wordclod(string, stop_words, filename):
   cloud = WordCloud(background_color="white", max_words=200, stopwords=set(stop_words), width=800, height=600)
   cloud.generate(string)
   cloud.to_file(filename)

# IMDB 
def get_random_top_movie():
    ia = imdb.IMDb()
    top = ia.get_top250_movies()
    return random.choice(top)

def get_top250():
    ia = imdb.IMDb()
    return ia.get_top250_movies()

# OpenSubtittles
def get_srt_from_imdb_id(imdb_id, language_id, location):
    ost = OpenSubtitles()
    ost.login(OPENSUBTITTLES_USER, OPENSUBTITTLES_PASS)
    print(f"Searching subtittles for IMDB Id: imdb_id={imdb_id}, language_id={language_id}")
    data = ost.search_subtitles([{'sublanguageid': language_id, 'imdbid': imdb_id}])
    print(f"Subtittles found: imdb_id={imdb_id}, language_id={language_id}, subtittles_count={len(data)}")
    sorted_subtittles = [v for v in sorted(data, key=lambda item: item['Score']*-1)]
    for subtittle in sorted_subtittles:
        id_subtitle_file = subtittle.get('IDSubtitleFile')
        print(f"Attempt to download subtittle: imdb_id={imdb_id}, subtittle_id={id_subtitle_file}")
        try:
            ost.download_subtitles([id_subtitle_file], output_directory=location, extension='srt')
            srt_filename = os.path.join(location, f"{id_subtitle_file}.srt")
            is_valid = False
            with open(srt_filename) as str_file:
                subtittle = open_srt(str_file)
            is_valid = True
        except srt.SRTParseError as error:
            print(error)
            os.remove(srt_filename)
            continue
        except UnicodeEncodeError as error:
            print(error)
            continue
        except FileNotFoundError:
            print(f"Subtittle download failed: subtittle_id={id_subtitle_file}")
            continue
        if is_valid:
            print(f"Valid subtittle found: subtittle_id={id_subtitle_file}")
            return id_subtitle_file
    print("Valid subtittle not found")

