"""
Evaluate a trained Word2Vec model against two testsets:
- Relationship Job -> Workplace
- Relationship Job -> Activities
"""
import csv
import logging
import os

import gensim

from src.util.globals import RESOURCE_DIR, MODELS_DIR
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

# load Word2Vec model trained on X28-Data
path = os.path.join(MODELS_DIR, 'semantic_model_x28.gz')
model_x28 = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
model_x28.init_sims(replace=True)

# load Word2Vec model trained on Fetchflow-Data
path = os.path.join(MODELS_DIR, 'semantic_model_fetchflow.gz')
model_ff = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
model_ff.init_sims(replace=True)


def evaluate_testset(testset_file, results_file):
    with open(testset_file, encoding='utf-8') as input, open(results_file, 'w', newline='') as output:
        csv_writer = csv.writer(output, dialect='excel', delimiter=';')
        lines = (line.strip() for line in input.readlines())

        for i, (job_1, wp_1, job_2, wp_2) in enumerate((line.split() for line in lines), 1):
            positives = [wp_1, job_2]
            negatives = [job_1]
            # prediction from X28-Model
            results_x28 = predict(model_x28, positives, negatives)
            results_x28 = ','.join(item for (item, _) in results_x28)
            # prediction from X28-Model
            results_ff = predict(model_ff, positives, negatives)
            results_ff = ','.join(item for (item, _) in results_ff)
            # write CSV
            row = [i, job_1, wp_1, job_2, wp_2, results_x28, results_ff]
            csv_writer.writerow(row)


def predict(model, positives, negatives):
    if set(positives + negatives).issubset(set(model.index2word)):
        return model.wv.most_similar(positives, negatives, 3)
    return []


if __name__ == '__main__':
    # check relation jobtitle -> workplace
    semantic_testset_workplace = os.path.join(RESOURCE_DIR, 'semantic_testset_workplace.txt')
    semantic_results_workplace = os.path.join(RESOURCE_DIR, 'word2vec_semantic_workplace.csv')
    evaluate_testset(semantic_testset_workplace, semantic_results_workplace)

    # check relation jobtitle -> activity
    semantic_testset_activity = os.path.join(RESOURCE_DIR, 'semantic_testset_activity.txt')
    semantic_results_activity = os.path.join(RESOURCE_DIR, 'word2vec_semantic_activity.csv')
    evaluate_testset(semantic_testset_activity, semantic_results_activity)
