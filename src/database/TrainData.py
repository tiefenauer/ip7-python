from src.database.data_source_split import SplitDataSource


class TrainData(SplitDataSource):

    def row_from(self, count, split):
        return None

    def row_to(self, count, split):
        return int(count * (split or 1))

    def num_rows(self, split):
        return self.row_to(self.count, split)
