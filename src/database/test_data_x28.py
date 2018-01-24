from src.database.entities_pg import X28_HTML
from src.database.test_data import TestData
from src.database.x28_german_data import X28GermanData


class X28TestData(TestData, X28GermanData):
    def __init__(self, args=None):
        super(X28TestData, self).__init__(X28_HTML, args)
