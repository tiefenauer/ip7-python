import math

from pony.orm import db_session

from src.database.data_source import DataSource

# number of rows to process in each page
pagesize = 1000


class PagingDataSource(DataSource):
    """iterates over data by paging. This has some serious performance advantages over the limit and offset approach
    with the disadvantage that the data cannot be split into training and test data (at least not easily).
    This means that this DataSource will contain ALL rows!
    """

    def __init__(self, args, Entity):
        super(PagingDataSource, self).__init__(args, Entity)
        # disable data splitting
        self.split = 1.0
        self.num_rows = self.num_total

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
