"""Reusable utility code."""
import os
import shutil

import requests
from django.core.exceptions import ObjectDoesNotExist

from movie_rating.secrets import MOVIE_DB_API_KEY
from ratings.models import Movie, Provider, Rating
from ratings.variables import IMAGE_SAVE_PATH, MOVIE_DB_IMAGE_URL, \
    MOVIE_DB_BASE_URL

PROVIDER_TYPES = ["rent", "buy", "flatrate"]


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


def process_new_movies(movies_list, original_movie=None):
    """Read list to save movies and get their posters."""
    movies = Movie.objects.all()
    existing_images = os.listdir(IMAGE_SAVE_PATH)
    movie_object_list = []

    for movie in movies_list:

        try:
            movie_object = movies.get(movie_id=movie['id'])
        except ObjectDoesNotExist:
            movie_object = Movie()

        movie_object.name = movie['title']
        movie_object.movie_id = movie['id']
        movie_object.language = movie['original_language']
        movie_object.description = movie['overview']
        movie_object.popularity = movie['popularity']
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
        try:
            tmdb_score = movie_object.ratings.get(service="Tmdb")
        except ObjectDoesNotExist:
            tmdb_score = Rating()
            tmdb_score.score = movie["vote_average"]
            tmdb_score.service = "Tmdb"
            tmdb_score.save()
            movie_object.ratings.add(tmdb_score)

        if movie_object.poster_id \
                and movie_object.poster_id \
                not in existing_images:
            save_image(movie_object.poster_id)

        movie_object_list.append(movie_object)

        # similar movies
        if original_movie is None:
            process_new_movies(
                url_request(
                    MOVIE_DB_BASE_URL,
                    "movie/{0}/similar".format(movie_object.movie_id)
                )["results"],
                original_movie=movie_object
            )

            providers = url_request(
                MOVIE_DB_BASE_URL,
                "movie/{0}/watch/providers".format(movie_object.movie_id)
            )["results"]
            try:
                for provider_type in providers["US"]:
                    if provider_type not in PROVIDER_TYPES:
                        continue
                    provider_list = Provider.objects.all()
                    for provider in providers["US"][provider_type]:
                        try:
                            provider_object = \
                                provider_list.get(
                                    name=provider["provider_name"]
                                )
                        except ObjectDoesNotExist:
                            provider_object = Provider()

                        provider_object.name = provider["provider_name"]
                        provider_object.poster_id = \
                            provider["logo_path"].replace("/", "")

                        provider_object.save()

                        movie_object.providers.add(provider_object)

                        if provider_object.poster_id \
                                and provider_object.poster_id \
                                not in existing_images:
                            save_image(provider_object.poster_id)
            except KeyError:
                pass

        else:
            movie_object.similar_movies.add(original_movie)

        # providers

    return movie_object_list
