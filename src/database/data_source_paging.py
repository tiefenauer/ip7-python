import math

from pony.orm import db_session

from src.database.data_source import DataSource

# number of rows to process in each page
pagesize = 1000


class PagingDataSource(DataSource):

    @db_session
    def __iter__(self):
        num_pages = int(math.ceil(self.num_rows / pagesize))
        query = self.Entity.select(lambda row: self.id < 0 or row.id == self.id)
        page_numbers = (i for i in range(1, num_pages))
        for page in (query.page(i, pagesize=pagesize) for i in page_numbers):
            for row in page:
                yield row

    @db_session
    def calc_num_rows(self, num_total, split):
        return self.Entity.select(lambda row: self.id < 0 or row.id == self.id).count()
