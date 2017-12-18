"""
A simple example of an animated plot
"""
import datetime
import logging
import time
from abc import abstractmethod

import matplotlib.pyplot as plt

from src.classifier.classifier import path_to_file
from src.evaluation.evaluation_plotter import EvaluationPlotter
from src.util import util

log = logging.getLogger(__name__)


class Evaluator(object):
    num_classified = 0

    def __init__(self, args, ResultEntity):
        self.visualize = args.visualize if hasattr(args, 'visualize') else False
        self.write = args.write if hasattr(args, 'write') else False
        if hasattr(args, 'truncate') and args.truncate:
            ResultEntity.truncate()

        self.ResultEntity = ResultEntity
        self.start_time = datetime.datetime.today()

    def evaluate(self, classifier, processed_data):
        # show plot
        if self.visualize:
            self.plotter = EvaluationPlotter(classifier.label(), self.get_scorers())

        num_total = processed_data.count
        num_processed = 0
        num_classified = 0

        for row, actual_class, predicted_class in classifier.classify(processed_data):
            num_processed += 1
            if self.is_classified(predicted_class):
                num_classified += 1
            scores = self.calculate_scores(actual_class, predicted_class)
            if self.visualize:
                self.plotter.update_plots(num_total, num_processed, num_classified)

            # only write results if not dry run and class could be predicted
            if self.write and predicted_class:
                self.ResultEntity.update_classification(row, predicted_class, scores)
                pass
        self.stop(classifier)

    def stop(self, classifier):
        filename = classifier.filename + '_' + time.strftime(util.DATE_PATTERN)
        path = path_to_file(filename)
        plt.savefig(path)

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
