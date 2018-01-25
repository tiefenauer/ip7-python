import argparse
import logging
import pickle

from src.classifier.jobtitle.jobtitle_classifier_structural import JobtitleStructuralClassifier
from src.database.test_data_x28 import X28TestData
from src.evaluation.evaluator_jobtitle_structural import StructuralEvaluator
from src.preprocessing.structural_preprocessor import StructuralPreprocessor
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
    # args.model = 'structural_model.gz' # old Naive Bayes
    args.model = 'multinomial.nb'

resource_dir = 'D:/code/ip7-python/resource/'
with open(resource_dir + args.model, 'rb') as modelfile, open(resource_dir + 'tfidf.vectorizer', 'rb') as vectorizerfile:
    model = pickle.load(modelfile)
    vectorizer = pickle.load(vectorizerfile)

if __name__ == '__main__':
    log.info('evaluating structural classifier')
    data_test = StructuralPreprocessor(X28TestData(args))
    classifier = JobtitleStructuralClassifier(model, vectorizer)
    evaluation = StructuralEvaluator(args)
    evaluation.evaluate(classifier, data_test)
    log.info('done!')
