import argparse

from src.classifier.loe.loe_classifier import LoeClassifier
from src.database.X28TrainData import X28TrainData
from src.evaluation.loe.evaluator_loe import LoeEvaluator
from src.preprocessing.loe_preprocessor import LoePreprocessor
from src.util.log_util import log_setup

parser = argparse.ArgumentParser(description="""Extract level of employment (LOE) - including evaluation""")
parser.add_argument('id', nargs='?', type=int,
                    help='(optional) id of single record to process. If set, only this record will be processed.')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

logging = log_setup()

if __name__ == '__main__':
    processed_data = LoePreprocessor(X28TrainData(args))
    classifier = LoeClassifier()
    evaluation = LoeEvaluator(args)
    evaluation.evaluate(classifier, processed_data)
