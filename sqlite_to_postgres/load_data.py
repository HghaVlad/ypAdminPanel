from uuid import UUID
from dataclasses import dataclass, fields
from datetime import datetime
import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


@dataclass
class FilmWork:
    id: UUID
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmWork:
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime


@dataclass
class Person:
    id: UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class PersonFilmWork:
    id: UUID
    film_work_id: UUID
    person_id: UUID
    created_at: datetime


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    cursor = connection.cursor()
    pg_cursor = pg_conn.cursor()
    """Основной метод загрузки данных из SQLite в Postgres"""
    for model, table in zip((FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork),
                            ("film_work", "genre", "genre_film_work", "person", "person_film_work")):

        columns = ",".join([field.name for field in fields(model)])
        try:
            cursor.execute(f"SELECT {columns} FROM {table}")
        except :
            print("Execution exception")
            return
        try:
            data = cursor.fetchall()
        except:
            print("Fetching data exception")

        try:
            args_str = ','.join(pg_cursor.mogrify('('+','.join("%s" for _ in range(len(fields(model)))) + ')', x).decode('utf-8') for x in data)
            pg_cursor.execute(f"INSERT INTO content.{table} ({columns}) VALUES {args_str} ON CONFLICT (id) DO NOTHING")
        except:
            print("INSERTING data exception")

        pg_conn.commit()


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
