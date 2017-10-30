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

    def __init__(self, evaluators=None):
        if evaluators:
            self.evaluators = evaluators

        num_plots = len(self.evaluators)
        ind = np.arange(1, num_plots + 1)
        self.plots = plt.bar(ind, [0] * num_plots)
        plt.show(block=False)

        ax.set_xticks(ind)
        ax.set_xticklabels([evaluator.label() for evaluator in self.evaluators])
        ax.set_xlabel('Evaluation methods')
        ax.set_ylim([0, 1])
        ax.set_ylabel('Accuracy')
        ax.set_title('Evaluation results')

        for i, plot in enumerate(self.plots):
            plot.set_facecolor(colors[i])

    def update(self, expected_class, predicted_class):
        for i, evaluator in enumerate(self.evaluators):
            evaluator.evaluate(expected_class, predicted_class)
            self.plots[i].set_height(evaluator.accuracy)
        fig.canvas.draw_idle()
        try:
            fig.canvas.flush_events()
        except NotImplementedError:
            pass
