import logging

from src.classifier.jobtitle_count_based import CountBasedJobTitleClassification
from src.classifier.jobtitle_feature_based import FeatureBasedJobTitleClassification
from src.classifier.jobtitle_title_based import TitleBasedJobTitleClassifier
from src.evaluation.evaluation import Evaluation
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator


def choose_evaluation(args):
    evaluators = []
    ev = TolerantJobtitleEvaluator()
    if args.evaluator == 'strict':
        evaluators.append(StrictEvaluator())
    if args.evaluator == 'linear':
        evaluators.append(LinearJobTitleEvaluator())
    logging.info('================================================')
    logging.info('Evaluation method(s): ' + ', '.join(e.title() for e in evaluators))
    logging.info('================================================')
    return Evaluation(evaluators)


def choose_classifier(args):
    classifier = FeatureBasedJobTitleClassification()
    if args.strategy == 'count':
        classifier = CountBasedJobTitleClassification()
    if args.strategy == 'title-based':
        classifier = TitleBasedJobTitleClassifier()
    logging.info('================================================')
    logging.info(classifier.title())
    logging.info(classifier.description())
    logging.info('================================================')
    return classifier