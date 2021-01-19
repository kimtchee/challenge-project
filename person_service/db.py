

def make_db_connection(config):
    pg_db = config['pg_db']
    pg_user = config['pg_user']
    pg_password = config['pg_password']
    import psycopg2
    import psycopg2.extras
    # Allow uuid as a type
    psycopg2.extras.register_uuid()
    try:
        conn = psycopg2.connect(
            dbname=pg_db, user=pg_user, password=pg_password)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return conn, cursor
    except Exception as e:
        print(e)
        print('Error connecting to db')
