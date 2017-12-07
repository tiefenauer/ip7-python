import logging

import matplotlib.pyplot as plt
import numpy as np

from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

classification_methods = [
    'fts',
    'semantic_rf',
    'semantic_avg',
    'structural_nv',
    'structural_nvt'
]


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom')


# https://matplotlib.org/examples/api/barchart_demo.html
def calculate_means():
    pass


if __name__ == '__main__':
    log.info('Visualizing evaluation results')
    N = len(classification_methods)
    strict_means = calculate_means()
    strict_means = (20, 35, 30, 35, 27)
    strict_std = (2, 3, 4, 1, 2)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, strict_means, width, color='r', yerr=strict_std)

    tolerant_means = (25, 32, 34, 20, 25)
    tolerant_std = (3, 5, 2, 3, 3)
    rects2 = ax.bar(ind + width, tolerant_means, width, color='b', yerr=tolerant_std)

    linear_means = (25, 32, 34, 20, 25)
    linear_std = (3, 5, 2, 3, 3)
    rects3 = ax.bar(ind + 2*width, linear_means, width, color='g', yerr=linear_std)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Average Score')
    ax.set_title('Scores by classification and score method')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((clf_name for clf_name in classification_methods))

    ax.legend((rects1[0], rects2[0], rects3[0]), ('strict', 'tolerant', 'linear'))

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.show()
