"""Management command to get popular movies."""
from django.core.management import BaseCommand

from ratings.utils import url_request, process_new_movies
from ratings.variables import MOVIE_DB_BASE_URL

MOVIE_PAGE_LIMIT = 11


def get_movies():
    """Get popular movies."""
    for page in range(1, MOVIE_PAGE_LIMIT):
        process_new_movies(
            url_request(
                MOVIE_DB_BASE_URL,
                "movie/popular", page
            )["results"]
        )


class Command(BaseCommand):
    """Command class for django."""

    help = 'Gets the top X movies from the movie db.'

    def handle(self, *args, **options):
        """Call module."""
        get_movies()
