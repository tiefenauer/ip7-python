from enum import Enum

import mysql.connector
import psycopg2


class Database(Enum):
    FETCHFLOW = 1,
    X28 = 2


# credentials
_config = {
    Database.FETCHFLOW: {
        'credentials': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': 'NAdu6004',
            'database': 'fetchflow'
        },
        'initializer': lambda cred: _create_mysql_connection(cred),
        'connection': None
    },
    Database.X28: {
        'credentials': {
            'host': '127.0.0.1',
            'user': 'postgres',
            'password': 'postgres',
            'database': 'x28'
        },
        'initializer': lambda cred: _create_postgres_connection(cred),
        'connection': None
    }
}


def connect_to(database):
    if _config[database]:
        credentials = _config[database]['credentials']
        initializer = _config[database]['initializer']
        return initializer(credentials)


def _create_mysql_connection(config):
    return mysql.connector.connect(user=config['user'], password=config['password'], host=config['host'],
                                   database=config['database'])


def _create_postgres_connection(config):
    return psycopg2.connect(host=config['host'], database=config['database'], user=config['user'],
                            password=config['password'])


def close(connection):
    if connection is not None:
        connection.close()