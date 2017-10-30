"""
A simple example of an animated plot
"""
import matplotlib.pyplot as plt
import numpy as np

from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator

fig, ax = plt.subplots()
ind = np.arange(1, 4)
p1, p2, p3 = plt.bar(ind, (0, 0, 0))
p1.set_facecolor('r')
p2.set_facecolor('g')
p3.set_facecolor('b')
ax.set_xticks(ind)
ax.set_ylim([0, 1])
ax.set_ylabel('Accuracy')
ax.set_title('Evaluation results')


class Evaluation(object):
    evaluators = [StrictEvaluator(), TolerantJobtitleEvaluator(), LinearJobTitleEvaluator()]

    def __init__(self, evaluators=None):
        if evaluators:
            self.evaluators = evaluators
        plt.show(block=False)
        ax.set_xticklabels([evaluator.title() for evaluator in self.evaluators])

    def update(self, expected_class, predicted_class):
        for evaluator in self.evaluators:
            evaluator.evaluate(expected_class, predicted_class)
        p1.set_height(self.evaluators[0].accuracy)
        p2.set_height(self.evaluators[1].accuracy)
        p3.set_height(self.evaluators[2].accuracy)
        fig.canvas.draw_idle()
        try:
            fig.canvas.flush_events()
        except NotImplementedError:
            pass
