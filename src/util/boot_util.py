import logging

from src.classifier.fts_classifier_jobtitle_count import CountBasedJobTitleClassification
from src.classifier.fts_classifier_jobtitle_features import FeatureBasedJobTitleClassifier
from src.classifier.fts_classifier_jobtitle_title import TitleBasedJobTitleClassifier
from src.evaluation.evaluation import Evaluation
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator

log = logging.getLogger(__name__)


def choose_evaluation(args, classifier):
    if not args.evaluator:
        return Evaluation(classifier)
    evaluators = []
    if args.evaluator == 'strict':
        evaluators.append(StrictEvaluator())
    if args.evaluator == 'linear':
        evaluators.append(LinearJobTitleEvaluator())
    log.info('================================================')
    log.info('Evaluation method(s): ' + ', '.join(e.title() for e in evaluators))
    log.info('================================================')
    return Evaluation(classifier)


def choose_classifier(args):
    classifier = FeatureBasedJobTitleClassifier()
    if args.strategy == 'count':
        classifier = CountBasedJobTitleClassification()
    if args.strategy == 'title-based':
        classifier = TitleBasedJobTitleClassifier()
    log.info('================================================')
    log.info(classifier.title())
    log.info(classifier.description())
    log.info('================================================')
    return classifier
