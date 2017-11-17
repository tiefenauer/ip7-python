import logging
import sys

from pony.orm import db_session

from src.database.entities_x28 import Data_Train

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class TrainingData(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @db_session
    def __init__(self, args):
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        self.split_from = args.offset if hasattr(args, 'offset') else 0
        self.split_to = args.limit if hasattr(args, 'limit') else 1
        self.num_total = Data_Train.select(lambda d: self.id < 0 or d.id == self.id).count()
        self.offset = int(self.num_total * self.split_from)
        self.limit = int(self.num_total * self.split_to)
        self.num_rows = self.limit - self.offset

    @db_session
    def __iter__(self):
        for row in Data_Train.select(lambda d: self.id < 0 or d.id == self.id):
            yield row

    def limit_offset(self, sql, parms):
        if self.split_from < 1:
            sql += ' OFFSET %(offset)s'
            parms['offset'] = self.offset  # 97204
        if self.split_to < 1:
            sql += ' LIMIT %(limit)s'
            parms['limit'] = self.limit  # 100
        return sql, parms
