import argparse
import logging

import nltk

from src.classifier.jobtitle.jobtitle_structural_classifier_nvt import JobtitleStructuralClassifierNVT
from src.database.X28TestData import X28TestData
from src.evaluation.jobtitle.evaluator_jobtitle_structural_nvt import StructuralNVTEvaluator
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using structural approach (nouns/verbs + HTML-Tag)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate')
parser.add_argument('id', nargs='?', type=int)
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
    args.model = 'structural_nvt_2017-11-27-18-05-11_19441rows.gz'

preprocessor = StructuralPreprocessorNVT()
classifier = JobtitleStructuralClassifierNVT(args)
evaluation = StructuralNVTEvaluator(args, classifier)

if __name__ == '__main__':
    log.info('evaluating structural classifier')
    data_test = X28TestData(args)
    evaluation.evaluate(data_test)
    log.info('evaluate_avg: done!')

    # some more evaluation with NLTK
    data_test = X28TestData(args)
    data_test_processed = preprocessor.preprocess(data_test, data_test.num_rows)
    test_set = ((classifier.extract_features(row.processed), row.title) for row in data_test_processed)
    nltk_accuracy = nltk.classify.accuracy(classifier.model, test_set)
    log.info('nltk.classify.accuracy: {}'.format(nltk_accuracy))
    log.info('classifier.show_most_informative_features(5):')
    classifier.model.show_most_informative_features(5)
