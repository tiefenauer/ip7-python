from src.database.data_source_split import SplitDataSource


class TestData(SplitDataSource):

    def row_from(self, count, split):
        return int(count * (split or 1))

    def row_to(self, count, split):
        return count

    def num_rows(self, split):
        return self.count - self.row_from(self.count, split)
