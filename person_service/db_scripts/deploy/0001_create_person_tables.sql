BEGIN;

DROP SCHEMA IF EXISTS people CASCADE;
CREATE SCHEMA IF NOT EXISTS people;

CREATE TABLE people.people_guids (
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
    person_id UUID PRIMARY KEY
);

CREATE TABLE people.people (
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  person_id UUID NOT NULL
    REFERENCES people.people_guids (person_id),
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  middle_name TEXT,
  email TEXT NOT NULL,
  age INTEGER NOT NULL,
  person_version SERIAL NOT NULL -- used for versioning
);

CREATE TABLE people.deleted_people (
  created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT now(),
  person_id UUID PRIMARY KEY
    REFERENCES people.people_guids (person_id)
);

COMMIT;

GRANT INSERT, UPDATE, SELECT, DELETE ON ALL TABLES
  IN SCHEMA people TO test;

GRANT ALL PRIVILEGES ON ALL SEQUENCES
  IN SCHEMA people TO test;

GRANT USAGE on SCHEMA people TO test;
