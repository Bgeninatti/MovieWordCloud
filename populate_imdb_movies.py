
from helpers import get_top250
from cfg import DB_PATH
from models import Movie, init_db


def download_top_250():
    init_db(DB_PATH)
    top_movies = get_top250()
    existing_movies = {m.imdb_id for m in Movie.select()}
    new_movies = [m for m in top_movies if m.movieID not in existing_movies]
    print(f"New movies found: new_movies={len(new_movies)}")
    for movie in new_movies:
        Movie.create(
            name=movie,
            year=movie.data['year'],
            imdb_id=movie.movieID
        )

if __name__ == '__main__':
    download_top_250()
