from src.database.entities_pg import X28_HTML
from src.database.train_data import TrainData
from src.database.x28_german_data import X28GermanData


class X28TrainData(TrainData, X28GermanData):
    def __init__(self, split=0.8):
        super(X28TrainData, self).__init__(X28_HTML, split)
