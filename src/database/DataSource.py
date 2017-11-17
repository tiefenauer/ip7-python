from abc import ABC

from pony.orm import db_session


class DataSource(ABC):
    @db_session
    def __init__(self, args, entity):
        self.Entity = entity
        # calculate total number of available rows
        self.id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        num_total = self.Entity.select(lambda d: self.id < 0 or d.id == self.id).count()
        self.num_total = num_total
        # calculate effective number of rows with limit and offset
        split_from = args.offset if hasattr(args, 'offset') else 0
        split_to = args.limit if hasattr(args, 'limit') else 1
        self.offset = int(num_total * split_from)
        self.limit = int(num_total * split_to)
        self.num_rows = self.limit - self.offset

    @db_session
    def __iter__(self):
        query = self.Entity.select(lambda d: self.id < 0 or d.id == self.id)
        self.limit_offset(query)
        for row in query:
            yield row

    def limit_offset(self, query):
        if self.limit > 0 and self.offset > 0:
            return query[self.offset:self.limit]
        elif self.offset > 0:
            return query[self.offset:]
        elif self.limit > 0:
            return query[:self.limit]
        return query