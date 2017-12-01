import argparse

from src.database.X28TrainData import X28TrainData
from src.extractor.loe_extractor import LoeExtractor
from src.preprocessing.fts_preprocessor import FtsPreprocessor
from src.util.log_util import log_setup

parser = argparse.ArgumentParser(description="""Extract level of employment (LOE) - including evaluation""")
parser.add_argument('source', nargs='?', choices=['fetchflow', 'x28'], default='x28',
                    help='(optional) data source to use. Default: X28')
parser.add_argument('id', nargs='?', type=int,
                    help='(optional) id of single record to process. If set, only this record will be processed.')
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for evaluation. Default: 1.0 (all data)')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

logging = log_setup()

x28_data = X28TrainData(args)
preprocessor = FtsPreprocessor()
extractor = LoeExtractor(args, preprocessor)

if __name__ == '__main__':
    extractor.process(x28_data)
