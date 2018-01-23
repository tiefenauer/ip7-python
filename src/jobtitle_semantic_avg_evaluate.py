import argparse
import logging

from src.classifier.jobtitle.jobtitle_semantic_classifier_avg import JobtitleSemanticClassifierAvg
from src.database.X28TestData import X28TestData
from src.database.entities_pg import Semantic_Avg_Classification_Results
from src.evaluation.jobtitle.evaluator_jobtitle_semantic_avg import SemanticAVGEvaluation
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate_avg')
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
    args.model = 'semantic_fetchflow_x28.gz'
    Semantic_Avg_Classification_Results._discriminator_ += '-fetchflow'
else:
    args.model = 'semantic_avg_x28.gz'
    Semantic_Avg_Classification_Results._discriminator_ += '-x28'

if __name__ == '__main__':
    log.info('evaluate_avg: evaluating Semantic Classifier by averaging vectors...')
    # remove stopwords for evaluation
    preprocessed_data = SemanticPreprocessor(X28TestData(args), remove_stopwords=True)
    classifier = JobtitleSemanticClassifierAvg(args)
    evaluation = SemanticAVGEvaluation(args)
    evaluation.evaluate(classifier, preprocessed_data)
    log.info('evaluate_avg: done!')
