"""
A simple example of an animated plot
"""
import matplotlib.pyplot as plt
import numpy as np

from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
fig, ax = plt.subplots()


class Evaluation(object):
    evaluators = [StrictEvaluator(), TolerantJobtitleEvaluator(), LinearJobTitleEvaluator()]

    def __init__(self, classifier, evaluators=None):
        fig.suptitle('Classification: ' + classifier.label())
        if evaluators:
            self.evaluators = evaluators

        num_plots = len(self.evaluators)
        ind = np.arange(1, num_plots + 1)
        self.plots = plt.bar(ind, [0] * num_plots)
        self.labels = [0, 0, 0]
        plt.show(block=False)

        ax.set_xticks(ind)
        ax.set_xticklabels([evaluator.label() for evaluator in self.evaluators])
        ax.set_xlabel('Evaluation methods')
        ax.set_ylim([0, 1])
        ax.set_ylabel('Average accuracy')

        for i, plot in enumerate(self.plots):
            plot.set_facecolor(colors[i])

    def update(self, expected_class, predicted_class, i, num_total):
        ax.set_title('after {}/{} processed items'.format(i, num_total))
        for i, evaluator in enumerate(self.evaluators):
            acc = evaluator.evaluate(expected_class, predicted_class)
            self.update_label(i, acc)
            self.plots[i].set_height(acc)
        fig.canvas.draw_idle()
        try:
            fig.canvas.flush_events()
        except NotImplementedError:
            pass

    def update_label(self, i, acc):
        if self.labels[i]:
            self.labels[i].remove()
        self.labels[i] = ax.text(i + .75, acc + 0.01, str("{:1.4f}".format(acc)), color='black', fontsize=10)
