from src.database.TrainData import TrainData
from src.database.entities_pg import X28_HTML


class X28TrainData(TrainData):
    def __init__(self, args):
        super(X28TrainData, self).__init__(args, X28_HTML)
