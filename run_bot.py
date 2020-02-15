import os
import json
import srt
from datetime import datetime
from helpers import (open_srt, tokenize_subtittle, get_stop_words, create_wordclod, get_top250)
from cfg import SRT_FOLDER, DEFAULT_LANGUAGE_ID, DB_PATH, OPENSUBTITTLES_USER, OPENSUBTITTLES_PASS, PNG_FOLDER
from models import Movie, init_db, get_next_movie
from opensubitles import OpenSubtitles


def create_wordcloud_for_next_movie():
    init_db(DB_PATH)
    movie = get_next_movie()

    print(f"Selected movie: Name={movie.name}, LanguageId={DEFAULT_LANGUAGE_ID}")
    with open(movie.srt_file, encoding="utf-8") as srt_file:
        subtittles = open_srt(srt_file)
    words = ' '.join(map(tokenize_subtittle, subtittles))
    stop_words = get_stop_words()
    destination = os.path.join(PNG_FOLDER, f"{movie.name} ({movie.year}).png")
    create_wordclod(words, stop_words, destination)
    movie.last_upload = datetime.now()
    movie.save()

def download_top_250():
    init_db(DB_PATH)
    os_client = OpenSubtitles(OPENSUBTITTLES_USER, OPENSUBTITTLES_PASS)
    top_movies = get_top250()
    existing_movies = {m.imdb_id for m in Movie.select()}
    new_movies = [m for m in top_movies if m.movieID not in existing_movies]
    print(f"New movies found: new_movies={len(new_movies)}")

    for movie in new_movies:
        all_subtitles = os_client.search_subtitles(movie.movieID, DEFAULT_LANGUAGE_ID)
        print("")
        print(f"Subtitles found: imdb_id={movie.movieID}, subtitles_count={len(all_subtitles)}")

        is_valid_subtitle = False
        while not is_valid_subtitle:
            try:
                sub = all_subtitles.pop()
                print(f"Attempt to download subtitle: subtitle_id={sub['IDSubtitleFile']}")
                srt_filename = os.path.join(SRT_FOLDER, f"{sub['IDSubtitleFile']}.srt")
                srt_file = os_client.download_subtitle(sub['SubDownloadLink'], "utf-8")
                subtitles = open_srt(srt_file)
                srt_file.seek(0)
                with open(srt_filename, "w") as srtf:
                    srtf.write(srt_file.read())
                is_valid_subtitle = True
                print(f"Download succeded")
            except srt.SRTParseError as error:
                if "Sorry, maximum download count for IP" in str(error):
                    print("API LIMIT REACHED!")
                    return
                print(error)
                continue
            except UnicodeEncodeError as error:
                print(error)
                continue
            except UnicodeDecodeError as error:
                print(error)
                continue
            except IndexError as error:
                print("No valid subtitle found")
                break
        Movie.create(
            name=movie,
            year=movie.data['year'],
            imdb_id=movie.movieID,
            opensubtittle_id=sub['IDSubtitleFile'],
            language_id=DEFAULT_LANGUAGE_ID,
            srt_file=srt_filename
        )

if __name__ == '__main__':
    # download_top_250()
    create_wordcloud_for_next_movie()
