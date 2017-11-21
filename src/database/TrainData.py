from src.database.DataSource import DataSource


class TrainData(DataSource):
    def create_cursor(self):
        return self.Entity.select()[:self.num_rows]

    def calc_num_rows(self, num_total, split):
        return int(num_total * split)