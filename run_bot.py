import os
import json
import srt
from helpers import (open_srt, tokenize_subtittle, get_most_common_words, create_wordclod, get_srt_from_imdb_id, get_random_top_movie, get_top250)
from nltk.corpus import stopwords
from cfg import SRT_FOLDER, DEFAULT_LANGUAGE_ID, DB_PATH
from models import Movie, init_db


def main():
    movie = get_random_top_movie()
    print(f"Selected movie: Name={movie.movieID}, LanguageId={DEFAULT_LANGUAGE_ID}")
    subtittle_id = get_srt_from_imdb_id(movie.movieID, DEFAULT_LANGUAGE_ID, SRT_FOLDER)
    with open(os.path.join(SRT_FOLDER, f"{subtittle_id}.srt"), encoding="ISO-8859-1") as srt_file:
        subtittles = open_srt(srt_file)
    words = ' '.join(map(tokenize_subtittle, subtittles))
    stop_words = stopwords.words('english') + get_most_common_words(words)
    create_wordclod(words, stop_words, f"{movie}.png")

def download_top_250():
    init_db(DB_PATH)
    movies = get_top250()
    full_words = ""
    for movie in movies:
        print("")
        subtittle_id = get_srt_from_imdb_id(movie.movieID, DEFAULT_LANGUAGE_ID, SRT_FOLDER)
        if subtittle_id is None:
            continue
        Movie.create(
            name=movie,
            imdb_id=movie.movieID,
            opensubtittle_id=subtittle_id,
            language_id=DEFAULT_LANGUAGE_ID,
            srt_file=os.path.join(SRT_FOLDER, f"{subtittle_id}.srt")
        )
        
        with open(os.path.join(SRT_FOLDER, f"{subtittle_id}.srt"), encoding="ISO-8859-1") as srt_file:
            subtittles = open_srt(srt_file)
        words = ' '.join(map(tokenize_subtittle, subtittles))
        full_words = f"{full_words} {words}"
    with open("full_words.txt", "w") as words_file:
        words_file.write(full_words)

if __name__ == '__main__':
    download_top_250()