"""Urls for movie rating."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include("ratings.urls", namespace="rating")
    )
]
