import math
from abc import ABC

from pony.orm import db_session


class DataSource(ABC):
    @db_session
    def __init__(self, args, entity):
        self.pagesize = 10
        self.Entity = entity
        # calculate total number of available rows
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        num_total = self.Entity.select(lambda d: self.id < 0 or d.id == self.id).count()
        self.num_total = num_total
        # calculate effective number of rows with limit and offset
        split = args.split if hasattr(args, 'split') else 1
        self.num_rows = int(num_total * split)

    @db_session
    def __iter__(self):
        num_pages = int(math.ceil(self.num_rows / self.pagesize))
        for page in (self.Entity.select().page(i+1, pagesize=self.pagesize) for i in (i for i in range(num_pages))):
            for row in page:
                yield row

    def create_cursor(self, rowid):
        return self.Entity.select(lambda d: d.id > rowid)[:self.pagesize]
