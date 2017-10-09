import db
import MySQLdb
from extractor import jobtitle
from db import Database

conn = db.connectTo(Database.FETCHFLOW)
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

batchsize = 100

cursor.execute('select count(*) from labeled_text')
count = cursor.fetchone()['count(*)']
for offset in range(0, count, batchsize):
    cursor.execute("select * from labeled_text limit %s offset %s", (batchsize, offset))
    for row in cursor:
        jobtitle.extractJobTitle(row)


