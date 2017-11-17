import argparse
import logging
import sys

from src.classifier.fts_classifier_jobtitle_count import CountBasedJobTitleClassification
from src.classifier.fts_classifier_jobtitle_features import FeatureBasedJobTitleClassifier
from src.classifier.fts_classifier_jobtitle_title import TitleBasedJobTitleClassifier
from src.evaluation.evaluation import Evaluation
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator


def set_up_logger():
    logger = logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s',
                                 level=logging.INFO)
    return logger


def parse_args():
    parser = argparse.ArgumentParser(description="""Train Semantic Classifier (Word2Vec)""")
    parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
    parser.add_argument('-l', '--limit', nargs='?', type=float, default=0.8,
                        help='(optional) fraction of labeled data to use for training')
    parser.add_argument('-o', '--offset', nargs='?', type=float, default=0.0,
                        help='(optional) fraction value of labeled data to start from')
    parser.add_argument('-m', '--model',
                        help='(optional) file with saved model to use. A new model will be created if not set.')
    return parser.parse_args()


def choose_evaluation(args, classifier):
    if not args.evaluator:
        return Evaluation(classifier)
    evaluators = []
    if args.evaluator == 'strict':
        evaluators.append(StrictEvaluator())
    if args.evaluator == 'linear':
        evaluators.append(LinearJobTitleEvaluator())
    logging.info('================================================')
    logging.info('Evaluation method(s): ' + ', '.join(e.title() for e in evaluators))
    logging.info('================================================')
    return Evaluation(classifier, evaluators)


def choose_classifier(args):
    classifier = FeatureBasedJobTitleClassifier()
    if args.strategy == 'count':
        classifier = CountBasedJobTitleClassification()
    if args.strategy == 'title-based':
        classifier = TitleBasedJobTitleClassifier()
    logging.info('================================================')
    logging.info(classifier.title())
    logging.info(classifier.description())
    logging.info('================================================')
    return classifier
