from src.database.TrainData import TrainData
from src.database.entities_pg import Fetchflow_HTML


class FetchflowTrainData(TrainData):
    def __init__(self, args):
        super(FetchflowTrainData, self).__init__(args, Fetchflow_HTML)
