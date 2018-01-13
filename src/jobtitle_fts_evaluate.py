import argparse
import logging

from src.classifier.jobtitle.jobtitle_fts_classifier_htmltag_based import FeatureBasedJobtitleFtsClassifier
from src.database.x28_data import X28Data
from src.evaluation.jobtitle.evaluator_jobtitle_fts import JobtitleFtsEvaluator
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor
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
parser.add_argument('-v', '--visualize', action='store_true',
                    help='(optional) visualize process by showing a live preview (default=False)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

if __name__ == '__main__':
    data_preprocessed = RelevantTagsPreprocessor(X28Data(args))
    classifier = FeatureBasedJobtitleFtsClassifier()
    evaluator = JobtitleFtsEvaluator(args)
    evaluator.evaluate(classifier, data_preprocessed)
