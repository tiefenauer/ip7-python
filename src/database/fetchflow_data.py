from src.database.data_source_paging import PagingDataSource
from src.database.entities_pg import Fetchflow_HTML


class FetchflowData(PagingDataSource):

    def __init__(self, args):
        super(FetchflowData, self).__init__(args, Fetchflow_HTML)
