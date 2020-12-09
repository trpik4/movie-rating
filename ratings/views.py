"""Views for rating."""
from django.views.generic import ListView, DetailView, CreateView

from ratings.models import Movie


class MovieListView(ListView):
    """Movie List View."""

    # Default template: movie_list.html
    queryset = Movie.objects.order_by("name")
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
