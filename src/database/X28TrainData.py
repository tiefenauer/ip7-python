from src.database.TrainData import TrainData
from src.database.entities_pg import X28_HTML
from src.database.x28_german_data import X28GermanData


class X28TrainData(TrainData, X28GermanData):
    def __init__(self, args):
        super(X28TrainData, self).__init__(args, X28_HTML)
