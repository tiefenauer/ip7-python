import logging
import sys

from src.database.DataSource import DataSource
from src.database.entities_pg import Data_Train

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class X28Data(DataSource):
    def __init__(self, args):
        super(X28Data, self).__init__(args, Data_Train)
