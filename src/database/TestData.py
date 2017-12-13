import math

from src.database.data_source_split import SplitDataSource


class TestData(SplitDataSource):

    def row_from(self):
        return self.split

    def row_to(self):
        return self.count

    def num_rows(self):
        return self.count - math.floor(self.count * self.split)
