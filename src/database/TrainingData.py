import logging
import sys

from src import db
from src.db import Database

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TrainingData(object):
    def __init__(self, args):
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        self.split_from = args.offset if hasattr(args, 'offset') else 0
        self.split_to = args.limit if hasattr(args, 'limit') else 1

    def __enter__(self):
        self.conn_read = db.connect_to(Database.X28_PG)
        self.conn_write = db.connect_to(Database.X28_PG)
        #
        cursor = self.conn_read.cursor()
        cursor.execute("""SELECT count(*) AS num_rows 
                          FROM data_train 
                          WHERE %(id)s < 0 OR id = %(id)s""",
                       {'id': self.id})
        self.num_total = cursor.fetchone()['num_rows']
        self.offset = int(self.num_total * self.split_from)
        self.limit = int(self.num_total * self.split_to)
        self.num_rows = self.limit - self.offset
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()
        self.conn_write.close()

    def __iter__(self):
        sql = """SELECT id, html, plaintext, url, title, x28_id 
                          FROM data_train
                          WHERE %(id)s < 0 OR id = %(id)s
                          """
        parms = {'id': self.id}
        sql, parms = self.limit_offset(sql, parms)

        cursor = self.conn_read.cursor()
        cursor.execute(sql, parms)
        for row in cursor:
            yield row

    def limit_offset(self, sql, parms):
        if self.split_from < 1:
            sql += ' OFFSET %(offset)s'
            parms['offset'] = self.offset  # 97204
        if self.split_to < 1:
            sql += ' LIMIT %(limit)s'
            parms['limit'] = self.limit  # 100
        return sql, parms
