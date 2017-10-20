import MySQLdb

from src import db
from src.db import Database
from src.extractor import jobtitle

conn = db.connectTo(Database.FETCHFLOW)
cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)

batchsize = 100

cursor.execute('select count(*) from labeled_text')
count = cursor.fetchone()['count(*)']
for offset in range(0, count, batchsize):
    cursor.execute("select * from labeled_text limit %s offset %s", (batchsize, offset))
    for row in cursor:
        jobtitle.extractJobTitle(row)


