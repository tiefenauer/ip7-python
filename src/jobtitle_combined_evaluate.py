import argparse
import logging

from src.classifier.jobtitle.jobtitle_combined_classifier import CombinedJobtitleClassifier
from src.database.x28_data import X28Data
from src.evaluation.jobtitle.evaluator_jobtitle_combined import JobtitleCombinedEvaluator
from src.preprocessing.sentence_preprocessor import SentencePreprocessor
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-c', '--calculate_score', type=bool, default=False,
                    help=""""(optional) calculate score on-the-fly. If set to True processing will be slower but 
                    score will already be calculated (default: False)""")
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=False)')
parser.add_argument('-v', '--visualize', action='store_true',
                    help='(optional) visualize process by showing a live preview (default=False)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

if __name__ == '__main__':
    processed_data = SentencePreprocessor(X28Data(args))
    classifier = CombinedJobtitleClassifier()
    evaluation = JobtitleCombinedEvaluator(args)
    evaluation.evaluate(classifier, processed_data)
