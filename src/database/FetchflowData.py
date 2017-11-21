from src.database.DataSource import DataSource
from src.database.entities_pg import Fetchflow_HTML


class FetchflowData(DataSource):
    def __init__(self, args):
        super(FetchflowData, self).__init__(args, Fetchflow_HTML)

    def create_cursor(self):
        return self.Entity.select()
