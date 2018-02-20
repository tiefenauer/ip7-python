from src.database.data_source_paging import PagingDataSource
from src.database.entities_pg import Fetchflow_HTML


class FetchflowTrainData(PagingDataSource):
    def __init__(self, row_id=None):
        super(FetchflowTrainData, self).__init__(Fetchflow_HTML, row_id)
