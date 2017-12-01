from enum import Enum

import psycopg2
from psycopg2.extras import DictCursor


class Database(Enum):
    X28_PG = 2,


# credentials
_config = {
    Database.X28_PG: {
        'credentials': {
            'host': '127.0.0.1',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'x28'
        },
        'initializer': lambda cred: _create_postgres_connection(cred),
        'connection': None
    },
}


def connect_to(database):
    if _config[database]:
        credentials = _config[database]['credentials']
        initializer = _config[database]['initializer']
        return initializer(credentials)


def _create_postgres_connection(config):
    return psycopg2.connect(host=config['host'], database=config['database'], user=config['user'],
                            password=config['password'], cursor_factory=DictCursor)
