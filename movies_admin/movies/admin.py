from django.contrib import admin
from .models import Genre, GenreFilmWork, FilmWork, Person, PersonFilmWork


# Register your models here.
class GenreFilmInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmInline(admin.TabularInline):
    model = PersonFilmWork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("title", "description")


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmInline, PersonFilmInline)

    list_display = ('title', 'type', 'creation_date', 'rating',)
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    list_display = ('full_name',)

