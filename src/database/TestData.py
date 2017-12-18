import math

from src.database.data_source_split import SplitDataSource


class TestData(SplitDataSource):

    def row_from(self):
        return math.ceil(self._split_row)

    def row_to(self):
        return self._count
