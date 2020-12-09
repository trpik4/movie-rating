"""Admin for ratings."""
from django.contrib import admin

from ratings.models import Movie, Rating, Person

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Person)
