"""
Evaluate the structural approach (NVT-variant) against X28-Data.
"""

import argparse
import gzip
import logging
import os
import pickle

from src.classifier.jobtitle.jobtitle_classifier_structural_nvt import JobtitleStructuralClassifierNVT
from src.database.test_data_x28 import X28TestData
from src.evaluation.evaluator_jobtitle_structural_nvt import StructuralNVTEvaluator
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT
from src.util.globals import MODELS_DIR
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
    args.model = 'structural_model_nvt.gz'

model_path = os.path.join(MODELS_DIR, args.model)
with gzip.open(model_path, 'rb') as f:
    model = pickle.load(f)

if __name__ == '__main__':
    log.info('evaluating structural classifier')
    data_test = StructuralPreprocessorNVT(X28TestData(args.split))
    classifier = JobtitleStructuralClassifierNVT(model)
    evaluation = StructuralNVTEvaluator(args)
    evaluation.evaluate(classifier, data_test)
    log.info('evaluate_avg: done!')
