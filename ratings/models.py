"""Models.py for ratings."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    """Person object."""

    name = models.CharField(
        _("name"),
        max_length=200,
        help_text=_("Name of the person."),
    )

    role = models.CharField(
        _("role"),
        max_length=200,
        help_text=_("Role of the person."),
    )

    def __str__(self):
        """Display name as string."""
        return str(self.name)


class Rating(models.Model):
    """Rating object."""

    score = models.IntegerField(
        _("score"),
        help_text=_("The number score of the movie.")
    )

    def __str__(self):
        """Display score as string."""
        return str(self.score)


class Movie(models.Model):
    """Movie object."""

    name = models.CharField(
        _("name"),
        max_length=200,
        help_text=_("Name of the movie."),
    )

    description = models.CharField(
        _("description"),
        max_length=200,
        help_text=_("Description of the movie.")
    )

    directors = models.ManyToManyField(
        Person,
        _("directors"),
        help_text=_("Directors of the movie.")
    )

    actors = models.ManyToManyField(
        Person,
        _("actors"),
        help_text=_("Actors in the movie.")
    )

    ratings = models.ManyToManyField(
        Rating,
        _("ratings"),
        help_text=_("Ratings for the movie.")
    )

    adult = models.BooleanField(
        _("adult"),
        help_text=_("Is this an adult movie?")
    )

    movie_id = models.IntegerField(
        _("Movie ids"),
        help_text=_("Id from movie database.")
    )

    language = models.CharField(
        _("language"),
        max_length=200,
        help_text=_("Language of the movie.")
    )

    release_date = models.DateField(
        _("release date"),
        help_text=_("Release date of the movie."),
        null=True
    )

    poster_id = models.CharField(
        _("Poster id"),
        max_length=200,
        help_text=_("Poster id of the movie."),
        null=True
    )

    def __str__(self):
        """Display name as string."""
        return str(self.name)
