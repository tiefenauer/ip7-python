from abc import abstractmethod

from pony.orm import db_session

from src.database.data_source import DataSource


class LimitOffsetDataSource(DataSource):

    @db_session
    def __iter__(self):
        for row in self.create_cursor():
            yield row

    @abstractmethod
    def create_cursor(self):
        """return a cursor for iteration over data"""
        return []
