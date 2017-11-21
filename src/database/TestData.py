from src.database.DataSource import DataSource


class TestData(DataSource):
    def __init__(self, args, Entity):
        super(TestData, self).__init__(args, Entity)

    def create_cursor(self):
        return self.Entity.select()[self.split:self.num_total]

    def calc_num_rows(self, num_total, split):
        return num_total - int(num_total * split)
