
from pathlib import Path


def init_db(conn):
    conn.set_session(autocommit=True)
    with conn.cursor() as cursor:
        cursor.execute(
            open(Path('person_service/db_scripts/deploy/0001_create_person_tables.sql'), 'r').read())


def destroy_db(conn):
    conn.set_session(autocommit=True)
    with conn.cursor() as cursor:
        cursor.execute(
            open(Path('person_service/db_scripts/rollback/0001_destroy_person_tables.sql'), 'r').read())


def create_fixtures(conn):
    conn.set_session(autocommit=True)
    with conn.cursor() as cursor:
        cursor.execute(
            open(Path('person_service/db_scripts/deploy/0002_create_person_fixtures.sql'), 'r').read())
