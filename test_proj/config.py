pg_user = 'test'
pg_db = 'challenge_db'
pg_password = 'test'


def make_db_connection():
    import psycopg2
    import psycopg2.extras
    # Allow uuid as a type
    psycopg2.extras.register_uuid()
    try:
        conn = psycopg2.connect(dbname=pg_db, user=pg_user, password=pg_password)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        return conn, cursor
    except:
        print('Error connecting to db')
