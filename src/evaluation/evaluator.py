"""
A simple example of an animated plot
"""
import datetime
import logging
import time
from abc import abstractmethod

import matplotlib.pyplot as plt

from src.evaluation.evaluation_plotter import EvaluationPlotter
from src.util import util

log = logging.getLogger(__name__)


class Evaluator(object):
    num_classified = 0

    def __init__(self, args, classifier, results):
        self.write = args.write if hasattr(args, 'write') else False
        if hasattr(args, 'truncate') and args.truncate:
            results.truncate()

        self.classifier = classifier
        self.results = results
        self.start_time = datetime.datetime.today()

        # show plot
        self.plotter = EvaluationPlotter(self)

    def evaluate(self, data_test):
        num_total = data_test.num_total
        num_processed = 0
        num_classified = 0

        for rowid, actual_class, predicted_class in self.classifier.classify_all(data_test):
            num_processed += 1
            if self.is_classified(predicted_class):
                num_classified += 1
            scores = self.calculate_scores(actual_class, predicted_class)
            self.plotter.update_plots(num_total, num_processed, num_classified)

            # only write results if not dry run and class could be predicted
            if self.write and predicted_class:
                self.results.update_classification(rowid, predicted_class, scores)
        self.stop()

    def stop(self):
        filename = self.classifier.filename + '_' + time.strftime(util.DATE_PATTERN)
        plt.savefig(filename)

    @abstractmethod
    def get_scorers(self):
        """return list of scorers for evaluation"""
        return []

    @abstractmethod
    def calculate_scores(self, actual_class, predicated_class):
        """return scores"""
        return ()

    @abstractmethod
    def is_classified(self, row):
        """update number of classified rows depending on result"""
        pass
