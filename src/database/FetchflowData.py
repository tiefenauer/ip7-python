from pony.orm import db_session
from tqdm import tqdm

from src import db
from src.database.entities_mysql_fetchflow import Labeled_Text
from src.db import Database


class FetchflowData(object):
    @db_session
    def __init__(self, args):
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        self.split_from = args.offset if hasattr(args, 'offset') else 0
        self.split_to = args.limit if hasattr(args, 'limit') else 1
        self.num_total = Labeled_Text.select(lambda d: self.id < 0 or d.id == self.id).count()
        self.offset = int(self.num_total * self.split_from)
        self.limit = int(self.num_total * self.split_to)
        self.num_rows = self.limit - self.offset

    def __enter__(self):
        self.conn_read = db.connect_to(Database.FETCHFLOW_MYSQL)
        self.conn_write = db.connect_to(Database.FETCHFLOW_MYSQL)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn_read.close()

    def __iter__(self):
        cursor = self.conn_read.cursor(dictionary=True)
        cursor.execute("SELECT id, title, CONVERT(contentbytes USING utf8) AS html FROM labeled_text")
        for row in tqdm(cursor, total=self.num_total, unit=' rows'):
            yield Row(row)

    def limit_offset(self, sql, parms):
        if self.split_from < 1:
            sql += ' OFFSET %(offset)s'
            parms['offset'] = self.offset  # 97204
        if self.split_to < 1:
            sql += ' LIMIT %(limit)s'
            parms['limit'] = self.limit  # 100
        return sql, parms


class Row(dict):
    def __init__(self, row):
        self.id = row['id']
        self.html = row['html']
