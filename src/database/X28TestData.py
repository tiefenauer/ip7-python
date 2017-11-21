import logging
import sys

from src.database.TestData import TestData
from src.database.entities_pg import X28_HTML

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class X28TestData(TestData):
    def __init__(self, args):
        super(X28TestData, self).__init__(args, X28_HTML)
