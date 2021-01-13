"""Views for rating."""
from django.views.generic import ListView, DetailView, CreateView

from ratings.models import Movie
from ratings.utils import url_request, process_new_movies
from ratings.variables import MOVIE_DB_BASE_URL


class MovieListView(ListView):
    """Movie List View."""

    # Default template: movie_list.html
    queryset = Movie.objects.order_by("-popularity")
    model = Movie
    context_object_name = "movies"


class MovieCreateView(CreateView):
    """Movie Create View."""

    # Default template: movie_form.html
    model = Movie
    context_object_name = "movie"
    fields = "__all__"


class MovieDetailView(DetailView):
    """Movie Detail View."""

    model = Movie
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        """Get context data for the movie."""
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context['similar_movies'] = process_new_movies(
            url_request(
                MOVIE_DB_BASE_URL,
                "movie/{0}/similar".format(context['movie'].movie_id)
            )['results'],
            original_movie=context['movie']
        )
        return context
