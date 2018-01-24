from src.database.data_source_paging import PagingDataSource
from src.database.entities_pg import X28_HTML
from src.database.x28_german_data import X28GermanData


class X28Data(PagingDataSource, X28GermanData):

    def __init__(self, args=None):
        super(X28Data, self).__init__(X28_HTML, args)
