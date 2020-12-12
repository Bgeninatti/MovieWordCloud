import click
from ..models import Movie
from .imdb import ImdbClient


@click.command()
@click.argument('ranking', type=str, default='all', required=True)
@click.argument('--save/--no-save', default=True)
def sync(ranking, save):
    imdb_client = ImdbClient()
    existing_movies = {m.imdb_id for m in Movie.select()}

    if ranking == 'top250':
        top250_movies = imdb_client.get_top250()
        new_movies = set(top250_movies).difference(existing_movies)
    elif ranking == 'most-populars':
        most_popular_ids = imdb_client.get_most_popular_movies_ids()
        new_movies_ids = set(most_popular_ids).difference(existing_movies)
        new_movies = []
        for imdb_id in new_movies_ids:
            new_movies.append(
                imdb_client.get_movie(imdb_id))
    else:
        raise ValueError("Ranking not recognized: {ranking}")

    if save:
        for movie in new_movies:
            Movie.create(
                name=movie,
                year=movie.data.get('year'),
                imdb_id=movie.movieID
            )
