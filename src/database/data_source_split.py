from abc import abstractmethod

from pony.orm import db_session

from src.database.data_source import DataSource


class SplitDataSource(DataSource):
    """Splits the given query into two parts for a given ratio. Only a part of the original query resultset
    is then used. Which par that is depends on the implementing class.
    """

    @db_session
    def __init__(self, Entity, split):
        super(SplitDataSource, self).__init__(Entity)
        self._count = self.query.count()

        # calculate row for split (will be part of first split)
        self._split_row = int((split or 1) * self._count)

        # split original query
        row_from = self.row_from()
        row_to = self.row_to()
        self.query = self.query[row_from:row_to]

    @db_session
    def __len__(self):
        return len(self.query)

    @abstractmethod
    def row_from(self):
        """return number of row that should be started from (offset)"""
        return None

    @abstractmethod
    def row_to(self):
        """return number of row until which should be iterated (offset + limit)"""
        return len(self)
