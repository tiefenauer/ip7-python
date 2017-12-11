import math

from src.database.data_source import DataSource
from src.database.data_source_limit_offset import LimitOffsetDataSource


class TrainData(LimitOffsetDataSource):
    def create_cursor(self):
        return self.Entity.select(lambda d: self.id < 0 or d.id == self.id)[:self.num_rows]

    def calc_num_rows(self, num_total, split):
        return math.ceil(num_total * split)