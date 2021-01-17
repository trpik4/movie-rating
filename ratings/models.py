"""Models.py for ratings."""
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class AbsoluteUrlFromClassNameMixin:
    """Mixin to return absolute url."""

    def get_absolute_url(self):
        """Return absolute url."""
        return reverse("rating:" + self.__class__.__name__.lower() + "_detail",
                       kwargs={"slug": self.slug})


class SlugFromNameMixin:
    """Mixin to generate slug from movie name."""

    def save(self, *args, **kwargs):
        """Override save to add slug."""
        if not self.pk or self.name != type(self)._base_manager.all()\
                .filter(pk=self.pk):
            self.slug = self.unique_slug()
        super().save(*args, **kwargs)

    def unique_slug(self):
        """Generate a unique slug."""
        try:
            origin_slug = slugify(self.name)
        except AttributeError:
            raise ImproperlyConfigured from AttributeError
        number = 1
        unique_slug = self.check_size(origin_slug, number)
        slug_qs = type(self)._base_manager.all().order_by().only("slug")\
            .exclude(pk=self.pk)
        slug_set = set(slug_qs.values_list("slug", flat=True))

        while unique_slug in slug_set:
            number += 1
            unique_slug = self.check_size(origin_slug, number)
        return unique_slug

    def check_size(self, origin_slug, numb):
        """Ensure slug size under 255."""
        new_slug = "{0}-{1}".format(origin_slug, numb)
        if len(new_slug) >= 255:
            return self.check_size(origin_slug[:-1], numb)
        return new_slug


class SlugFromNameModel(SlugFromNameMixin, models.Model):
    """Abstract class that adds slug."""

    slug = models.SlugField(
        max_length=255,
        editable=False
    )

    class Meta:
        """Meta class."""

        abstract = True


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


class Movie(SlugFromNameModel, AbsoluteUrlFromClassNameMixin):
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

    popularity = models.FloatField(
        _("Popularity"),
        help_text=_("Popularity of the movie.")
    )

    similar_movies = models.ManyToManyField(
        "self",
        blank=True,
        help_text=_("Similar movies.")
    )

    providers = models.ManyToManyField(
        "Provider",
        blank=True,
        help_text=_("Providers of movie.")
    )

    def __str__(self):
        """Display name as string."""
        return str(self.name)

class Provider(SlugFromNameModel):

    name = models.CharField(
        _("name"),
        max_length=200,
        help_text=_("Name of the movie."),
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
