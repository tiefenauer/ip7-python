"""
A simple example of an animated plot
"""
import datetime
import time

import matplotlib.pyplot as plt
import numpy as np

from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator
from src.util import util

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

fig, ax = plt.subplots(figsize=(8, 8))
bar_width = 0.35


def create_figure(classifier):
    fig.suptitle('Classification: ' + classifier.label())
    plt.show(block=False)


def create_plots(evaluators):
    num_plots = len(evaluators)
    ind = np.arange(num_plots)
    acc1_plots = ax.bar(ind, [0] * num_plots, bar_width, color='b')
    acc2_plots = ax.bar(ind + bar_width, [0] * num_plots, bar_width, color='g')
    labels = [0] * num_plots * 2

    ax.set_xticks(ind + bar_width / 2)
    ax.set_xticklabels([evaluator.label() for evaluator in evaluators])
    ax.set_xlabel('Evaluation methods')
    ax.set_ylim([0, 1])
    ax.set_ylabel('Average accuracy')
    ax.legend((acc1_plots[0], acc2_plots[0]), ('Accuracy if classifiable', 'Overall accuracy'))
    return acc1_plots, acc2_plots, labels


def update_title(num_processed, num_total, num_classified):
    percent_classified = 100 * num_classified / num_processed
    title = """
    after {num_processed}/{num_total} processed items
    {num_classified}/{num_processed} ({percent_classified}) items classified
    """.format(num_classified=num_classified,
               num_processed=num_processed,
               num_total=num_total,
               percent_classified="{:1.2f}%".format(percent_classified)
               )
    ax.set_title(title)


class Evaluation(object):
    num_classified = 0

    def __init__(self, classifier, results):
        self.classifier = classifier
        self.results = results
        self.start_time = datetime.datetime.today()
        create_figure(classifier)
        self.evaluator_strict = StrictEvaluator()
        self.evaluator_tolerant = TolerantJobtitleEvaluator()
        self.evaluator_linear = LinearJobTitleEvaluator()
        self.evaluators = [self.evaluator_strict, self.evaluator_tolerant, self.evaluator_linear]
        self.acc1_plots, self.acc2_plots, self.labels = create_plots(self.evaluators)

    def evaluate(self, data_test):
        for i, row in enumerate(self.classifier.classify(data_test), 1):
            sc_str, sc_tol, sc_lin = self.update(row.title, row.predicted_class, i, data_test.num_rows)
            self.results.update_classification(row, row.predicted_class, sc_str, sc_tol, sc_lin)
        self.stop()

    def update(self, expected_class, predicted_class, i, num_total):
        if predicted_class and len(predicted_class) > 0:
            self.num_classified += 1

        score_strict = self.evaluator_strict.evaluate(expected_class, predicted_class)
        score_tolerant = self.evaluator_tolerant.evaluate(expected_class, predicted_class)
        score_linear = self.evaluator_linear.evaluate(expected_class, predicted_class)
        update_title(i, num_total, self.num_classified)
        self.update_plots(expected_class, predicted_class)
        fig.canvas.draw_idle()
        try:
            fig.canvas.flush_events()
        except NotImplementedError:
            pass
        return score_strict, score_tolerant, score_linear

    def update_plots(self, expected_class, predicted_class):
        for i, evaluator in enumerate(self.evaluators):
            acc = evaluator.accuracy
            overall_acc = evaluator.overall_accuracy
            self.acc1_plots[i].set_height(acc)
            self.acc2_plots[i].set_height(overall_acc)
            self.update_label(i, acc)
            self.update_label(i + 1, overall_acc)

    def update_label(self, i, height):
        if self.labels[i]:
            self.labels[i].remove()
        x = i + (i % 2) * 0.5 * bar_width
        y = 1.01 * height
        text = str("{:1.4f}".format(height))
        self.labels[i] = ax.text(x, y, text, ha='center', va='bottom', color='black', fontsize=10)

    def stop(self):
        filename = self.classifier.model_file
        filename += '_' + time.strftime(util.DATE_PATTERN)
        plt.savefig(filename)
