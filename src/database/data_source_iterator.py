from pony.orm import db_session
from tqdm import tqdm

from src.database.data_source import DataSource


class IteratoRrDataSource(DataSource):
    """According to this post this is an efficient method for iterating over large datasets:
    https://github.com/ponyorm/pony/issues/210
    """

    @db_session
    def __iter__(self):
        query = self.create_query()
        count = query.count()
        for i in tqdm(range(count), unit=' rows'):
            row = query[i:(i + 1)][0]
            yield row

    @db_session
    def create_query(self):
        pass

    def calc_num_rows(self, num_total, split):
        pass