import logging

from src.classifier.fts_classifier_jobtitle_count import CountBasedJobTitleClassification
from src.classifier.fts_classifier_jobtitle_features import FeatureBasedJobTitleClassifier
from src.classifier.fts_classifier_jobtitle_title import TitleBasedJobTitleClassifier
from src.evaluation.evaluation import Evaluation
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator


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