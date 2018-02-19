from abc import ABC

from pony.orm import db_session


class DataSource(ABC):
    """Base class for all data source. A data source represents rows of a certain entity."""

    @db_session
    def __init__(self, Entity, row_id=None):
        self.Entity = Entity
        self.row_id = row_id
        self.query = self.create_query()

    @db_session
    def __iter__(self):
        for row in self.query:
            yield row

    @db_session
    def __len__(self):
        return self.query.count()

    def create_query(self):
        """create Pony ORM query"""
        return self.Entity.select(lambda row: self.row_id is None or row.id == self.row_id)
