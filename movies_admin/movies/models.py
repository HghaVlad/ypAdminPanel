import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("FullName"), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _("person")
        verbose_name_plural = _("People")

    def __str__(self):
        return self.full_name


class TypeChoice(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(_("creation_date"), blank=True, null=True)
    rating = models.FloatField(_("rating"), blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.TextField(_("type"), choices=TypeChoice.choices)

    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    persons = models.ManyToManyField(Person, through="PersonFilmWork")

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _("film")
        verbose_name_plural = _("films")

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    film_work = models.ForeignKey("FilmWork", on_delete=models.CASCADE)
    role = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
