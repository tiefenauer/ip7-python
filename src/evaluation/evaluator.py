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

        for row in self.classifier.classify_all(data_test):
            num_processed += 1
            if self.is_classified(row):
                num_classified += 1
            self.plotter.update_plots(num_total, num_processed, num_classified)

            # only write results if not dry run and class could be predicted
            if self.write and row.predicted_class:
                scores = self.calculate_scores(row)
                self.results.update_classification(row, scores)
        self.stop()

    def stop(self):
        filename = self.classifier.filename + '_' + time.strftime(util.DATE_PATTERN)
        plt.savefig(filename)

    @abstractmethod
    def get_scorers(self):
        """return list of scorers for evaluation"""
        return []

    @abstractmethod
    def calculate_scores(self, row):
        """return scores"""
        return ()

    @abstractmethod
    def is_classified(self, row):
        """update number of classified rows depending on result"""
        pass
