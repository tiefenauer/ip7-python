import math

from src.database.data_source_limit_offset import LimitOffsetDataSource


class TestData(LimitOffsetDataSource):
    def __init__(self, args, Entity):
        super(TestData, self).__init__(args, Entity)

    def create_cursor(self):
        return self.Entity.select(lambda d: self.id < 0 or d.id == self.id)[self.split:self.num_total]

    def calc_num_rows(self, num_total, split):
        return num_total - math.floor(num_total * split)
