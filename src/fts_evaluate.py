import argparse
import logging
import sys

from tqdm import tqdm

from src import preproc
from src.classifier.fts_classifier_jobtitle_count import CountBasedJobTitleClassification
from src.classifier.fts_classifier_jobtitle_features import FeatureBasedJobTitleClassifier
from src.classifier.fts_classifier_jobtitle_title import TitleBasedJobTitleClassifier
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator
from src.importer.data_train import TrainingData
from src.preprocessing.preprocessor_fts import FtsX28Preprocessor
from src.util.boot_util import choose_classifier, choose_evaluation

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
    with TrainingData(args) as data_train:
        for i, (row_id, expected_class, relevant_tags) in enumerate(preprocessor.preprocess(data_train), 1):
            predicted_class = classifier.classify(relevant_tags)
            sc_str, sc_tol, sc_lin = evaluation.update(expected_class, predicted_class, i, data_train.num_rows)
            data_train.classify_job(row_id, predicted_class, sc_str, sc_tol, sc_lin)
            evaluation.stop()
