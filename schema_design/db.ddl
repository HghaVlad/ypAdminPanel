CREATE SCHEMA content;

SET search_path to content;


create table if not exists content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

create table if not exists content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

create table if not exists content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

create table if not exists content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid REFERENCES content.genre (id),
    film_work_id uuid REFERENCES content.film_work (id),
    created timestamp with time zone
);

create table if not exists content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid REFERENCES content.person (id),
    film_work_id uuid REFERENCES content.film_work (id),
    role TEXT ,
    created timestamp with time zone
);


CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);

CREATE INDEX ON content.film_work (creation_date, rating)
