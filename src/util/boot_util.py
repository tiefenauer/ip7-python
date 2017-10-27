import logging

from src.classifier.jobtitle_strategy_count import CountBasedJobTitleClassification
from src.classifier.jobtitle_strategy_feature_based import FeatureBasedJobTitleClassification
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator


def choose_evaluator(args):
    ev = TolerantJobtitleEvaluator()
    if args.evaluator == 'strict':
        ev = StrictEvaluator()
    logging.info('================================================')
    logging.info(ev.title())
    logging.info(ev.description())
    logging.info('================================================')
    return ev


def choose_strategy(args):
    classifier = FeatureBasedJobTitleClassification()
    if args.strategy == 'count':
        classifier = CountBasedJobTitleClassification()
    logging.info('================================================')
    logging.info(classifier.title())
    logging.info(classifier.description())
    logging.info('================================================')
    return classifier