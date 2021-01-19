BEGIN;

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
