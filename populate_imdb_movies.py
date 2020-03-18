import imdb
from helpers import get_top250, get_most_popular_movies_ids
from cfg import DB_PATH
from models import Movie, init_db


def download_top_250(excluded_movies_ids):
    top_movies = get_top250()
    new_movies = [m for m in top_movies if m.movieID not in excluded_movies_ids]
    print(f"New movies found in top 250: new_movies={len(new_movies)}")
    for movie in new_movies:
        print(f"Adding movie to database: name={movie}, imdb_id={movie.movieID}")
        Movie.create(
            name=movie,
            year=movie.data['year'],
            imdb_id=movie.movieID
        )

def download_most_populars(excluded_movies_ids):
    ia = imdb.IMDb()
    popular_movies = get_most_popular_movies_ids()
    new_movies = [m for m in popular_movies if m not in excluded_movies_ids]
    print(f"New movies found in most populars: new_movies={len(new_movies)}")
    for m_id in new_movies:
        movie = ia.get_movie(m_id)
        print(f"Adding movie to database: name={movie}, imdb_id={movie.movieID}")
        Movie.create(
            name=movie,
            year=movie.data['year'],
            imdb_id=movie.movieID
        )


if __name__ == '__main__':
    init_db(DB_PATH)
    existing_movies = {m.imdb_id for m in Movie.select()}
    download_top_250(existing_movies)
    download_most_populars(existing_movies)
