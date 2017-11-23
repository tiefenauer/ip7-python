import argparse
import logging

from tqdm import tqdm

from src.classifier.fts_classifier_jobtitle_count import CountBasedJobTitleClassification
from src.classifier.fts_classifier_jobtitle_features import FeatureBasedJobTitleClassifier
from src.classifier.fts_classifier_jobtitle_title import TitleBasedJobTitleClassifier
from src.database.ClassificationResults import FtsClassificationResults
from src.database.X28TestData import X28TestData
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator
from src.preprocessing.preprocessor_fts import FtsX28Preprocessor
from src.util.boot_util import choose_classifier, choose_evaluation, log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-e', '--evaluator', choices=['strict', 'tolerant', 'linear'],
                    help="""method to use to evaluate_avg the predicted class. 
                    - 'strict': {}
                    - 'tolerant': {}
                    - 'linear': {}
                    """.format(StrictEvaluator.DESCRIPTION,
                               TolerantJobtitleEvaluator.DESCRIPTION,
                               LinearJobTitleEvaluator.DESCRIPTION))
parser.add_argument('-s', '--strategy', choices=['count', 'feature-based', 'title-based'], default='feature-based',
                    help="""strategy used for classification:
                    - 'count': {}
                    - 'feature-based': {}
                    - 'title-based': {}
                    """.format(CountBasedJobTitleClassification.DESCRIPTION,
                               FeatureBasedJobTitleClassifier.DESCRIPTION,
                               TitleBasedJobTitleClassifier.DESCRIPTION
                               ))
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

preprocessor = FtsX28Preprocessor()
classifier = choose_classifier(args)
evaluation = choose_evaluation(args, classifier)

if __name__ == '__main__':
    data_train = X28TestData(args)
    results = FtsClassificationResults(args)

    for i, row in enumerate(tqdm(preprocessor.preprocess(data_train), total=data_train.num_rows, unit=' rows'), 1):
        predicted_class = classifier.classify(row.processed)
        sc_str, sc_tol, sc_lin = evaluation.update(row.title, predicted_class, i, data_train.num_rows)
        results.update_classification(row, predicted_class, sc_str, sc_tol, sc_lin)
        evaluation.stop()
