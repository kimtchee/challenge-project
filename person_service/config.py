import os
from dotenv import load_dotenv


def get_config(cf_path=None):
    if not cf_path:
        load_dotenv()
    else:
        load_dotenv(cf_path)
    return {
        'pg_user': os.environ.get('pg_user'),
        'pg_db': os.environ.get('pg_db'),
        'pg_password': os.environ.get('pg_password')
    }


__all__ = ['get_config']
