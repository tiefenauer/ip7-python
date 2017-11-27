import math

from src.database.DataSource import DataSource


class TrainData(DataSource):
    def create_cursor(self):
        return self.Entity.select(lambda d: self.id < 0 or d.id == self.id)[:self.num_rows]

    def calc_num_rows(self, num_total, split):
        return math.ceil(num_total * split)