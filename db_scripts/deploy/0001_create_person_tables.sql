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

INSERT INTO people.people_guids (person_id)
  VALUES ('ceb5770f-c4e3-4ad7-bc5e-4e32e8047e63'),
  ('ea6869c1-5c84-4d69-8993-7d3cdc24c0ee'),
  ('8da79d7f-76d8-4c8a-8cab-0e1671d2d44d'),
  ('213988f1-e9bd-4eba-8609-45ce16de82b7');

INSERT INTO people.people (person_id, first_name, middle_name, last_name, age, email)
  VALUES ('ceb5770f-c4e3-4ad7-bc5e-4e32e8047e63', 'Mary', 'Eugene', 'Smith', 40, 'maryeugenesmith@email.com'),
  ('ea6869c1-5c84-4d69-8993-7d3cdc24c0ee', 'Ellen', null, 'Egrot', 40, 'ellenegrot@email.com'),
  ('8da79d7f-76d8-4c8a-8cab-0e1671d2d44d', 'Roger', null, 'Gunn', 40, 'rogergunn@email.com');

INSERT INTO people.deleted_people (person_id) VALUES ('213988f1-e9bd-4eba-8609-45ce16de82b7');


COMMIT;

GRANT INSERT, UPDATE, SELECT, DELETE ON ALL TABLES
  IN SCHEMA people TO test;

GRANT ALL PRIVILEGES ON ALL SEQUENCES
  IN SCHEMA people TO test;

GRANT USAGE on SCHEMA people TO test;
