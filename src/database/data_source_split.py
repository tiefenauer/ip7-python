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
        self._count = self.query.count()

        # calculate row for split (will be part of first split)
        split = args.split if hasattr(args, 'split') and args.split else 1
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
