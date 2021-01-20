
from pathlib import Path
import psycopg2


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


if __name__ == '__main__':
    from people_service.config import get_config
    conn, cursor = db.make_db_connection(config=get_config())
    try:
        init_db(conn)
        create_fixtures(conn)
    except psycopg2.errors.lookup('42501') as e:
        print(e)
        print('Requires postgres superuser or create schema privilege')
    print('Created db')
