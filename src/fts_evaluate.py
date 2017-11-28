import argparse
import logging

from src.classifier.fts_classifier_jobtitle_features import FeatureBasedJobTitleClassifier
from src.database.ClassificationResults import FtsClassificationResults
from src.database.X28TestData import X28TestData
from src.evaluation.evaluation import Evaluation
from src.evaluation.evaluation_fts import FtsEvaluation
from src.preprocessing.preprocessor_fts import FtsPreprocessor
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

preprocessor = FtsPreprocessor()
classifier = FeatureBasedJobTitleClassifier(args, preprocessor)
evaluation = FtsEvaluation(args, classifier)

if __name__ == '__main__':
    data_train = X28TestData(args)
    evaluation.evaluate(data_train)
