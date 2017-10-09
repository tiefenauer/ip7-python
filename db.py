import MySQLdb
from enum import Enum


class Database(Enum):
    FETCHFLOW = 1

# credentials
fetchflow = {
    'hostname': 'localhost',
    'username': 'root',
    'password': 'NAdu6004',
    'database': 'fetchflow'
}

_conn_fetchflow = None


# Simple routine to run a query on a database and print the results:
def executeQuery(query, conn):
    cur = conn.cursor()

    cur.execute(query)

    for firstname, lastname in cur.fetchall():
        print(firstname, lastname)

def connectTo(database):
    if database == Database.FETCHFLOW:
        return createConnection(_conn_fetchflow, fetchflow)

def close(connection):
    if connection is not None:
        connection.close()

def createConnection(conn, credentials):
    if conn is None:
        conn = MySQLdb.connect(host=credentials['hostname'], user=credentials['username'], passwd=credentials['password'],
                                   db=credentials['database'])
    return conn

#db_fetchflow = MySQLdb.connect(host=fetchflow['hostname'], user=fetchflow['username'], passwd=fetchflow['password'],
#                               db=fetchflow['database'])

#db_fetchflow.close()


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
