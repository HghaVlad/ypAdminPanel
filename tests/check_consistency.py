import sqlite3
import psycopg2
from dataclasses import fields
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_to_postgres.load_data import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


def test(connection: sqlite3.Connection, pg_conn: _connection):
    cursor = connection.cursor()
    pg_cursor = pg_conn.cursor()
    # Number of rows
    for table in ("film_work", "genre", "genre_film_work", "person", "person_film_work"):
        cursor.execute(f"SELECT count(*) FROM {table}")
        count = cursor.fetchone()[0]
        pg_cursor.execute(f"SELECT count(*) FROM content.{table}")
        pg_count = pg_cursor.fetchone()[0]
        assert count == pg_count, f"The number of rows in {table} exception"

    # The contents of entries
    for model, table in zip((FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork),
                            ("film_work", "genre", "genre_film_work", "person", "person_film_work")):
        columns = ",".join([field.name for field in fields(model)])
        cursor.execute(f"SELECT {columns} FROM {table}")
        data = cursor.fetchall()
        pg_cursor.execute(f"SELECT {columns} FROM content.{table}")
        pg_data = pg_cursor.fetchall()
        for row, pg_row in zip(data, pg_data):
            instance = model(*row)
            pg_instance = model(*row)
            assert instance == pg_instance


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        test(sqlite_conn, pg_conn)


