import argparse
import logging

from src.classifier.jobtitle.jobtitle_combined_classifier import CombinedJobtitleClassifier
from src.database.X28TrainData import X28TrainData
from src.evaluation.jobtitle.evaluator_jobtitle_combined import JobtitleCombinedEvaluator
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

classifier = CombinedJobtitleClassifier(args)
evaluation = JobtitleCombinedEvaluator(args, classifier)

if __name__ == '__main__':
    data_train = X28TrainData(args)
    evaluation.evaluate(data_train)
