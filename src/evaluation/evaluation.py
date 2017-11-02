"""
A simple example of an animated plot
"""
import datetime
import matplotlib.pyplot as plt
import numpy as np

from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator

all_evaluators = [StrictEvaluator(), TolerantJobtitleEvaluator(), LinearJobTitleEvaluator()]
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']

fig, ax = plt.subplots(figsize=(8,8))


def create_figure(classifier):
    fig.suptitle('Classification: ' + classifier.label())
    plt.show(block=False)


def create_plots(evaluators):
    num_plots = len(evaluators)
    ind = np.arange(1, num_plots + 1)
    plots = plt.bar(ind, [0] * num_plots)
    for i, plot in enumerate(plots):
        plot.set_facecolor(colors[i])
    labels = [0, 0, 0]

    ax.set_xticks(ind)
    ax.set_xticklabels([evaluator.label() for evaluator in evaluators])
    ax.set_xlabel('Evaluation methods')
    ax.set_ylim([0, 1])
    ax.set_ylabel('Average accuracy')
    return plots, labels


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

    def __init__(self, classifier, evaluators=all_evaluators):
        self.start_time = datetime.datetime.today()
        create_figure(classifier)
        self.evaluators = evaluators
        self.plots, self.labels = create_plots(evaluators)

    def update(self, expected_class, predicted_class, i, num_total):
        if predicted_class and len(predicted_class) > 0:
            self.num_classified += 1

        update_title(i, num_total, self.num_classified)
        self.update_plots(expected_class, predicted_class)
        fig.canvas.draw_idle()
        try:
            fig.canvas.flush_events()
        except NotImplementedError:
            pass

    def update_plots(self, expected_class, predicted_class):
        for i, evaluator in enumerate(self.evaluators):
            acc = evaluator.evaluate(expected_class, predicted_class)
            self.update_label(i, acc)
            self.plots[i].set_height(acc)

    def update_label(self, i, acc):
        if self.labels[i]:
            self.labels[i].remove()
        self.labels[i] = ax.text(i + .75, acc + 0.01, str("{:1.4f}".format(acc)), color='black', fontsize=10)

    def stop(self):
        filename = self.start_time.strftime('%Y-%m-%d-%H-%M-%S')
        plt.savefig(filename)