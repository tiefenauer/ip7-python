import argparse
import logging

from src.classifier.structural_classifier import StructuralClassifier
from src.database.ClassificationResults import StructuralClassificationResults
from src.database.X28TestData import X28TestData
from src.evaluation.evaluation import Evaluation
from src.preprocessing.preprocessor_structural import StructuralPreprocessor
from src.util.boot_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate_avg')
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training/testing')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")

args = parser.parse_args()

if not args.model:
    args.model = 'structural_nv_2017-11-24-14-29-31.gz'

data_test = X28TestData(args)
preprocessor = StructuralPreprocessor()
classifier = StructuralClassifier(args, preprocessor)
evaluation = Evaluation(classifier)
results = StructuralClassificationResults(args, classifier)
model = classifier.model

if __name__ == '__main__':
    log.info('evaluating structural classifier')

    for i, row in enumerate(preprocessor.preprocess(data_test, data_test.num_rows), 1):
        predicted_class = classifier.classify(row.processed)
        sc_str, sc_tol, sc_lin = evaluation.update(row.title, predicted_class, i, data_test.num_rows)
        results.update_classification(row, predicted_class, sc_str, sc_tol, sc_lin)
    evaluation.stop()
    log.info('evaluate_avg: done!')
