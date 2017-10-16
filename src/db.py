from enum import Enum
import mysql.connector


class Database(Enum):
    FETCHFLOW = 1


_config = {
    Database.FETCHFLOW: {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'NAdu6004',
        'database': 'fetchflow'
    }
}
# credentials

_conn_fetchflow = None


def connectTo(database):
    return createConnection(_conn_fetchflow, _config[database])


def createConnection(conn, config):
    if conn is None:
        conn = mysql.connector.connect(user=config['user'], password=config['password'], host=config['host'], database=config['database'])
    return conn


def close(connection):
    if connection is not None:
        connection.close()

# db_fetchflow = MySQLdb.connect(host=fetchflow['hostname'], user=fetchflow['username'], passwd=fetchflow['password'],
#                               db=fetchflow['database'])

# db_fetchflow.close()


# print "Using pymysql…"
# import pymysql
# myConnection = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
# doQuery( myConnection )
# myConnection.close()
#
# print "Using mysql.connector…"
# import mysql.connector
# myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database )
# doQuery( myConnection )
# myConnection.close()
