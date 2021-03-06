"""
Evaluate the semantic approach against X28-Data.
"""
import argparse
import logging
import os
import pickle

import gensim

from src.classifier.jobtitle.jobtitle_classifier_semantic import JobtitleSemanticClassifier
from src.database.entities_pg import Semantic_Classification_Results
from src.database.test_data_x28 import X28TestData
from src.evaluation.evaluator_jobtitle_semantic import SemanticEvaluation
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from src.util.globals import MODELS_DIR
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate')
parser.add_argument('-c', '--calculate_score', type=bool, default=True,
                    help=""""(optional) calculate score on-the-fly. If set to Fals processing might be a bit faster 
                    but score will need to calculated manually afterwards (default: True)""")
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training/testing')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-v', '--visualize', action='store_true',
                    help='(optional) visualize process by showing a live preview (default=False)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

if args.model == 'fetchflow':
    args.model = 'semantic_model_fetchflow.gz'
    Semantic_Classification_Results._discriminator_ += '-fetchflow'
else:
    args.model = 'semantic_model_x28.gz'
    Semantic_Classification_Results._discriminator_ += '-x28'

model_path = os.path.join(MODELS_DIR, args.model)
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)

if __name__ == '__main__':
    log.info('evaluating Semantic Classifier by averaging vectors...')
    # remove stopwords for evaluation
    preprocessed_data = SemanticPreprocessor(X28TestData(args.split), remove_stopwords=True)
    classifier = JobtitleSemanticClassifier(model)
    evaluation = SemanticEvaluation(args)
    evaluation.evaluate(classifier, preprocessed_data)
    log.info('done!')
