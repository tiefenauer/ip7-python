import math

from src.database.data_source_split import SplitDataSource


class TrainData(SplitDataSource):

    def row_from(self):
        return None

    def row_to(self):
        return int(math.floor(self._split_row))
