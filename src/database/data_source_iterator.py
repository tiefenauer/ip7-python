from pony.orm import db_session

from src.database.data_source import DataSource


class IteratorDataSource(DataSource):
    """According to this post this is an efficient method for iterating over large datasets:
    https://github.com/ponyorm/pony/issues/210
    """

    @db_session
    def __iter__(self):
        for i in range(self.count):
            row = self.query[i:(i + 1)][0]
            yield row
