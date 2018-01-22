# evaluates a word2vec model
import csv
import logging
import os

import gensim
from pony.orm import commit, db_session
from tqdm import tqdm

from src.database.entities_pg import Job_Class_To_Job_Class_Similar, Job_Class_Similar, Job_Class
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

resource_dir = 'D:/code/ip7-python/resource/'
model_dir = resource_dir + 'models'
semantic_testset_workplace = resource_dir + 'semantic_testset_workplace.txt'
semantic_testset_activity = resource_dir + 'semantic_testset_activity.txt'

# load Word2Vec model trained on X28-Data
model_x28_name = 'semantic_avg_x28.gz'
path = os.path.join(model_dir, model_x28_name)
model_x28 = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
model_x28.init_sims(replace=True)
x28_index2word = set(model_x28.index2word)

# load Word2Vec model trained on Fetchflow-Data
model_fetchflow_name = 'semantic_avg_fetchflow.gz'
path = os.path.join(model_dir, model_fetchflow_name)
model_ff = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)
model_ff.init_sims(replace=True)
fetchflow_index2word = set(model_ff.index2word)


def predict(model, positives, negatives):
    if set(positives + negatives).issubset(set(model.index2word)):
        return model.wv.most_similar(positives, negatives, 3)
    return []


with open(semantic_testset_workplace, encoding='utf-8') as input, \
        open('word2vec_semantic_workplace.csv', 'w', newline='') as output:
    csv_writer = csv.writer(output, dialect='excel', delimiter=';')
    lines = (line.strip() for line in input.readlines())
    for i, (job_1, wp_1, job_2, wp_actual) in enumerate((line.split() for line in lines), 1):
        positives = [wp_1, job_2]
        negatives = [job_1]
        # prediction from X28-Model
        results_x28 = predict(model_x28, positives, negatives)
        wp_2_x28 = ','.join(item for (item, _) in results_x28)
        # prediction from X28-Model
        results_ff = predict(model_ff, positives, negatives)
        wp_2_ff = ','.join(item for (item, _) in results_ff)

        row = [i, job_1, wp_1, job_2, wp_actual, wp_2_x28, wp_2_ff]
        print(''.join(str(cell).ljust(50) for cell in row))
        # wp_actual = '\n'.join(wp_actual.split(','))
        csv_writer.writerow(row)


def doesnt_match(words):
    print('Doesn\'t match: ' + words)
    result = model_x28.doesnt_match(words.split())
    print(result)


def most_similar(word):
    if word not in x28_index2word:
        return
    print('Most similar: ' + word)
    row_format = "{:>30} {}"
    for result, score in model_x28.wv.most_similar(word):
        print(row_format.format(result, score))


def update_most_similar_job_classes():
    log.info('update_most_similar_job_classes: Updating DB with most similar jobs for trained jobs...')
    with db_session:
        # truncate previous mappings
        Job_Class_To_Job_Class_Similar.select().delete(bulk=True)
        Job_Class_Similar.select().delete(bulk=True)
        commit()
        # add new mappings
        known_and_trained_jobs = list(job_class for job_class in Job_Class.select()
                                      if job_class.job_name in model_x28.index2word)

        for job_class in tqdm(known_and_trained_jobs, unit=' rows'):
            for similar_name, score in model_x28.most_similar(job_class.job_name):
                if Job_Class_Similar.exists(job_name_similar=similar_name):
                    job_class_similar = Job_Class_Similar.get(job_name_similar=similar_name)
                else:
                    job_class_similar = Job_Class_Similar(job_name_similar=similar_name)
                commit()
                Job_Class_To_Job_Class_Similar(fk_job_class=job_class.id, fk_job_class_similar=job_class_similar.id,
                                               score=score)
    log.info('update_most_similar_job_classes: done!')

# semantic_testset = [
#     # Arbeitsorte
#     ('Koch', 'Küche', 'Mechaniker', 'Werkstatt'),
#     # ('Koch', 'Küche', 'Lehrer', 'Schule'),
# ]
# for w0, w1, w2, w3 in semantic_testset:
#     results = model.wv.most_similar([w1, w2], [w0], 5)
#     string = w2 + ': ' + ', '.join(item for (item, score) in results)
#     print(string)
#
# for job_name in (job_name for job_name in KnownJobs() if job_name in index2word_set):
#     results = model.wv.most_similar(['Küche', job_name], ['Koch'], 5)
#     string = job_name + ': ' + ', '.join(item for (item, score) in results)
#     print(string)
#
# for job_name in (job_name for job_name in KnownJobs() if job_name in index2word_set):
#     results = model.wv.most_similar(['kochen', job_name], ['Koch'], 5)
#     string = job_name + ': ' + ', '.join(item for (item, score) in results)
#     print(string)
#
# for job_name in KnownJobs():
#     most_similar(job_name)
