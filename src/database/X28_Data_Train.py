import logging
import sys

from src.database.DataSource import DataSource
from src.database.entities_x28 import Data_Train

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class X28_Data_Train(DataSource):
    def __init__(self, args):
        super(X28_Data_Train, self).__init__(args, Data_Train)
