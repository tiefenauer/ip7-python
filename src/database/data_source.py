from abc import ABC

from pony.orm import db_session


class DataSource(ABC):
    @db_session
    def __init__(self, args, Entity):
        self.Entity = Entity
        self.query = self.create_query(args)
        self.count = self.query.count()

    @db_session
    def __iter__(self):
        for row in self.query:
            yield row

    def create_query(self, args):
        """create Pony ORM query"""
        where_clause = self.create_where_clause(args)
        return self.Entity.select(where_clause)

    def create_where_clause(self, args):
        id = args.id if hasattr(args, 'id') and args.id is not None else -1000
        return lambda row: id < 0 or row.id == id
