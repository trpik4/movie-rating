"""Urls for ratings."""
from django.urls import path

from ratings import views

urlpatterns = [
    path(
        '',
        views.MovieListView.as_view(),
        name="movie_list"
    ),
    path(
        'movies/',
        views.MovieListView.as_view(),
        name="movie_list"
    ),
    path(
        'movies/add/',
        views.MovieCreateView.as_view(),
        name="movie_create"
    ),
    path(
        'movies/<str:slug>/',
        views.MovieDetailView.as_view(),
        name="movie_detail"
    )
]

app_name = "ratings"
