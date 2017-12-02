import matplotlib.pyplot as plt
import numpy as np

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
fig, ax = plt.subplots(figsize=(8, 8))
bar_width = 0.35


def create_figure(title):
    fig.suptitle('Classification: ' + title)
    plt.show(block=False)


def create_plots(xlabels):
    num_plots = len(xlabels)
    ind = np.arange(num_plots)
    plots1 = ax.bar(ind, [0] * num_plots, bar_width, color='b')
    plots2 = ax.bar(ind + bar_width, [0] * num_plots, bar_width, color='g')

    ax.set_xticks(ind + bar_width / 2)
    ax.set_xticklabels(xlabels)
    ax.set_xlabel('Evaluation methods')
    ax.set_ylim([0, 1])
    ax.set_ylabel('Average accuracy')
    ax.legend((plots1[0], plots2[0]), ('Accuracy if classifiable', 'Overall accuracy'))
    return plots1, plots2


def update_figure(num_processed, num_total, num_classified):
    update_title(num_processed, num_total, num_classified)
    fig.canvas.draw_idle()
    try:
        fig.canvas.flush_events()
    except NotImplementedError:
        pass


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


class EvaluationPlotter(object):

    def __init__(self, evaluator):
        self.evaluator = evaluator

        title = evaluator.classifier.label()
        xlabels = [scorer.label() for scorer in evaluator.get_scorers()]

        create_figure(title)

        num_plots = len(xlabels)
        self.plots1, self.plots2 = create_plots(xlabels)
        self.labels = [0] * num_plots * 2

    def update_plots(self, num_total, num_processed, num_classified):
        update_figure(num_processed, num_total, num_classified)

        for i, scorer in enumerate(self.evaluator.get_scorers()):
            acc = scorer.accuracy
            overall_acc = scorer.overall_accuracy

            self.plots1[i].set_height(acc)
            self.plots2[i].set_height(overall_acc)

            self.update_label(i, acc)
            self.update_label(i + 1, overall_acc)

    def update_label(self, i, height):
        if self.labels[i]:
            self.labels[i].remove()
        x = i + (i % 2) * 0.5 * bar_width
        y = 1.01 * height
        text = str("{:1.4f}".format(height))
        self.labels[i] = ax.text(x, y, text, ha='center', va='bottom', color='black', fontsize=10)
