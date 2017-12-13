import math

from src.database.data_source_split import SplitDataSource


class TrainData(SplitDataSource):

    def row_from(self):
        return None

    def row_to(self):
        return self.split

    def num_rows(self):
        return math.ceil(self.count * self.split)
