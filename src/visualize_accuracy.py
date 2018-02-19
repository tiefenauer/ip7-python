import argparse
import logging
import subprocess

import matplotlib.pyplot as plt
import numpy as np
from pony.orm import db_session

from src.database.entities_pg import Classification_Results
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Plot statistics for classification method""")
args = parser.parse_args()

classification_methods = [
    'jobtitle-fts',
    'jobtitle-combined',
    # 'jobtitle-semantic',
    # 'jobtitle-semantic-x28',
    # 'jobtitle-semantic-fetchflow',
    # 'jobtitle-structural-nv',
    # 'jobtitle-structural-nvt',
    # 'jobtitle-structural',
    # 'loe-fts'
]


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.001 * height,
                '{0:.3f}'.format(height),
                ha='center', va='bottom', size=7)


# https://matplotlib.org/examples/api/barchart_demo.html
@db_session
def calculate_means_std(score_method):
    means = []
    std = []
    for method in classification_methods:
        query = Classification_Results.select(lambda x: x.clf_method == method)
        if query.count() == 0:
            means.append(0)
            std.append(0)
        else:
            score_name = 'score_' + score_method
            scores = np.array([getattr(row, score_name) for row in query])
            means.append(np.mean(scores))
            std.append(np.std(scores))
    return means, std


if __name__ == '__main__':
    log.info('Visualizing accuracy')
    N = len(classification_methods)
    means_strict, std_strict = calculate_means_std('strict')
    means_tolerant, std_tolerant = calculate_means_std('tolerant')
    means_linear, std_linear = calculate_means_std('linear')

    ind = np.arange(N)  # the x locations for the groups
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=(16, 8))
    rects1 = ax.bar(ind - width / 2, means_strict, width, color='r')
    rects2 = ax.bar(ind + width / 2, means_tolerant, width, color='b')
    rects3 = ax.bar(ind + 3 * width / 2, means_linear, width, color='g')

    # add some text for labels, title and axes ticks
    git_commit = subprocess.check_output(["git", "describe", '--always'], cwd='..').strip()
    ax.set_title('Accuracy by classification and score method\nGit commit: ' + git_commit.decode('utf-8'))
    ax.set_ylabel('Average accuracy')
    ax.set_xticks(ind + width / 2)

    # labels: classification method + number of evaluated rows
    nums = ['N/A' for _ in classification_methods]
    with db_session:
        for i, method in enumerate(classification_methods):
            nums[i] = Classification_Results.select(lambda x: x.clf_method == method).count()
    ax.set_xticklabels(
        (clf_name + '\n' + str(num) + " vacancies classified" for clf_name, num in zip(classification_methods, nums)))

    ax.legend((rects1[0], rects2[0], rects3[0]), ('strict', 'tolerant', 'linear'))

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    plt.show()
