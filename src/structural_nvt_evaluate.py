import argparse
import logging

import nltk

from src.classifier.structural_classifier_nvt import StructuralClassifierNVT
from src.database.ClassificationResults import StructuralClassificationNVTResults
from src.database.X28TestData import X28TestData
from src.evaluation.evaluation import Evaluation
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT
from src.util.boot_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using structural approach (nouns/verbs + HTML-Tag)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate')
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
    args.model = 'structural_nv_2017-11-24-14-51-03_19rows.gz'

data_test = X28TestData(args)
preprocessor = StructuralPreprocessorNVT()
classifier = StructuralClassifierNVT(args, preprocessor)
evaluation = Evaluation(classifier)
results = StructuralClassificationNVTResults(args, classifier)

if __name__ == '__main__':
    log.info('evaluating structural classifier')

    for i, row in enumerate(preprocessor.preprocess(data_test, data_test.num_rows), 1):
        predicted_class = classifier.classify(row.processed)
        sc_str, sc_tol, sc_lin = evaluation.update(row.title, predicted_class, i, data_test.num_rows)
        results.update_classification(row, predicted_class, sc_str, sc_tol, sc_lin)
    evaluation.stop()
    log.info('evaluate_avg: done!')

    # some more evaluation with NLTK
    data_test = X28TestData(args)
    test_set = preprocessor.preprocess(data_test, data_test.num_rows)
    nltk_accuracy = nltk.classify.accuracy(classifier.model, test_set)
    log.info('nltk.classify.accuracy: {}'.format(nltk_accuracy))
    log.info('classifier.show_most_informative_features(5):')
    classifier.model.show_most_informative_features(5)
