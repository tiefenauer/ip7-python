from abc import ABC, abstractmethod

from src import db
from src.db import Database


class Entity(ABC):
    def __init__(self):
        self.table_name = self.get_table_name()

    def __enter__(self):
        self.conn = db.connect_to(Database.X28_PG)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def __iter__(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM {}""".format(self.table_name))
        for row in cursor:
            yield row

    def insert(self, **kwargs):
        pony
        for key, value in kwargs:
            if key not in self.get_table_rows():
                raise ValidationError

    @abstractmethod
    def get_table_name(self):
        """return the table name of the implementing entity"""

    @abstractmethod
    def get_table_rows(self):
