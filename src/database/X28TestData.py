from src.database.TestData import TestData
from src.database.entities_pg import X28_HTML


class X28TestData(TestData):
    def __init__(self, args):
        super(X28TestData, self).__init__(args, X28_HTML)
