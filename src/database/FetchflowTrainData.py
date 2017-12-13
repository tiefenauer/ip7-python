from src.database.data_source import DataSource
from src.database.entities_pg import Fetchflow_HTML


class FetchflowTrainData(DataSource):
    def __init__(self, args):
        super(FetchflowTrainData, self).__init__(args, Fetchflow_HTML)
