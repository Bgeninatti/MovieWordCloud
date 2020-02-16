
import os
import srt
from helpers import open_srt
from cfg import (SRT_FOLDER, DEFAULT_LANGUAGE_ID, DB_PATH, OPENSUBTITTLES_USER,
                 OPENSUBTITTLES_PASS)
from models import Movie, init_db
from opensubitles import OpenSubtitles

def download_subtitles():
    init_db(DB_PATH)
    movies = Movie.select().where(Movie.opensubtittle_id.is_null())
    os_client = OpenSubtitles(OPENSUBTITTLES_USER, OPENSUBTITTLES_PASS)
    print(f"Movies with missing subtitles: movies_count={len(movies)}")

    for movie in movies:
        all_subtitles = os_client.search_subtitles(movie.imdb_id, DEFAULT_LANGUAGE_ID)
        print("")
        print(f"Subtitles found: imdb_id={movie.imdb_id}, subtitles_count={len(all_subtitles)}")

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

        movie.opensubtittle_id = sub['IDSubtitleFile'],
        movie.language_id = DEFAULT_LANGUAGE_ID,
        movie.srt_file = srt_filename
        movie.save()

if __name__ == '__main__':
    download_subtitles()
