from src.database.data_source_paging import PagingDataSource
from src.database.entities_pg import X28_HTML


class X28Data(PagingDataSource):

    def __init__(self, args):
        super(X28Data, self).__init__(args, X28_HTML)
