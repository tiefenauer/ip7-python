from abc import abstractmethod

from pony.orm import db_session

from src.database.data_source import DataSource


class SplitDataSource(DataSource):
    """Splits the given query into two parts by evaluating the ratio in args.split. Only a part of the original query
    is then used. Which par that is depends on the implementing class
    """

    @db_session
    def __init__(self, args, Entity):
        super(SplitDataSource, self).__init__(args, Entity)
        split = args.split if hasattr(args, 'split') and args.split else 1
        # split data
        self.query = self.query[self.row_from(self.count, split):self.row_to(self.count, split)]
        # update count with effective count
        self.count = self.num_rows(split)

    @abstractmethod
    def row_from(self, count, split):
        """return number of row that should be started from (offset)"""
        return None

    @abstractmethod
    def row_to(self, count, split):
        """return number of row until which should be iterated (offset + limit)"""
        return self.count

    @abstractmethod
    def num_rows(self, split):
        """calculate number of rows to process with current splitting"""
        return self.count
