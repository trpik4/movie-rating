"""Management command to get popular movies."""
import os
import shutil

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
import requests

from movie_rating.secrets import MOVIE_DB_API_KEY
from ratings.models import Movie

MOVIE_DB_BASE_URL = "https://api.themoviedb.org/3/"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/original/"
IMAGE_SAVE_PATH = "static/images/"
MOVIE_PAGE_LIMIT = 10


def url_request(url, url_params="", page=1):
    """Get url request."""
    get_request = requests.get(
        url + url_params,
        params={'api_key': MOVIE_DB_API_KEY, 'page': page}
    )

    assert get_request.status_code == 200

    return get_request.json()


def save_image(poster_id):
    """Save image."""
    image_request = requests.get(MOVIE_DB_IMAGE_URL + poster_id, stream=True)

    if image_request.status_code == 200:
        image_request.raw.decode_content = True

        with open(IMAGE_SAVE_PATH + poster_id, 'wb') as file:
            shutil.copyfileobj(image_request.raw, file)


def get_images():
    """Get images from poster id."""
    movies = Movie.objects.all().values_list("poster_id", flat=True)
    existing_images = os.listdir(IMAGE_SAVE_PATH)
    for poster_id in movies:
        if poster_id not in existing_images and poster_id is not None:
            save_image(poster_id)


def get_movies():
    """Get popular movies."""
    movies = Movie.objects.all()

    for page in range(1, MOVIE_PAGE_LIMIT):
        for movie in url_request(
                MOVIE_DB_BASE_URL,
                "movie/popular", page
        )["results"]:
            try:
                movie_object = movies.get(movie_id=movie['id'])
            except ObjectDoesNotExist:
                movie_object = Movie()

            movie_object.name = movie['title']
            movie_object.movie_id = movie['id']
            movie_object.language = movie['original_language']
            movie_object.description = movie['overview']
            try:
                if len(movie['release_date']) > 0:
                    movie_object.release_date = movie['release_date']
            except KeyError:
                pass
            movie_object.adult = movie['adult']
            try:
                movie_object.poster_id = movie['poster_path'].replace("/", "")
            except AttributeError:
                pass
            movie_object.save()


class Command(BaseCommand):
    """Command class for django."""

    help = 'Gets the top X movies from the movie db.'

    def handle(self, *args, **options):
        """Call module."""
        get_movies()
        get_images()
