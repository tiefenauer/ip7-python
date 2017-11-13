import argparse
import logging
import sys

import pony.orm as pny
from pony.orm import commit
from tqdm import tqdm

from src.classifier.semantic_classifier import SemanticClassifier
from src.database.data_classification_results import ClassificationResults
from src.database.data_train import TrainingData
from src.database.entities import Job_Class_Similar, Job_Class, Job_Class_To_Job_Class_Similar
from src.evaluation.evaluation import Evaluation
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate_avg')
parser.add_argument('-l', '--limit', nargs='?', type=float, default=1.0,
                    help='(optional) fraction of labeled data to use for training')
parser.add_argument('-o', '--offset', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to start from')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")

args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

preprocessor = SemanticX28Preprocessor(remove_stopwords=True)  # remove stopwords for evaluation

if not args.model:
    args.model = '2017-11-13-07-57-49_300features_40minwords_10context.gz'


def doesnt_match(words):
    print('Doesn\'t match: ' + words)
    result = model.doesnt_match(words.split())
    print(result)


def most_similar(word):
    print('Most similar: ' + word)
    row_format = "{:>30} {}"
    for result, score in model.most_similar(word):
        print(row_format.format(result, score))


def update_most_similar_job_classes():
    logging.info('update_most_similar_job_classes: Updating DB with most similar jobs for trained jobs...')
    with pny.db_session:
        # truncate previous mappings
        Job_Class_To_Job_Class_Similar.select().delete(bulk=True)
        Job_Class_Similar.select().delete(bulk=True)
        commit()
        # add new mappings
        known_and_trained_jobs = list(
            job_class for job_class in Job_Class.select() if job_class.job_name in model.index2word)
        for job_class in tqdm(known_and_trained_jobs, unit=' rows'):
            for similar_name, score in model.most_similar(job_class.job_name):
                if Job_Class_Similar.exists(job_name_similar=similar_name):
                    job_class_similar = Job_Class_Similar.get(job_name_similar=similar_name)
                else:
                    job_class_similar = Job_Class_Similar(job_name_similar=similar_name)
                commit()
                Job_Class_To_Job_Class_Similar(fk_job_class=job_class.id, fk_job_class_similar=job_class_similar.id,
                                               score=score)
    logging.info('update_most_similar_job_classes: done!')


def evaluate_avg(clf):
    logging.info('evaluate_avg: evaluating Semantic Classifier by averaging vectors...')
    evaluation = Evaluation(clf)
    with TrainingData(args) as data_train, ClassificationResults('semantic_avg', args) as results:
        i = 0
        for row_id, actual_class, sentences in ((row_id, actual_class, sents) for (row_id, actual_class, sents) in
                                                preprocessor.preprocess(data_train)):
            i += 1
            predicted_class = clf.classify(sentences)
            sc_str, sc_tol, sc_lin = evaluation.update(actual_class, predicted_class, i, data_train.num_rows)
            results.update_classification(row_id, predicted_class, sc_str, sc_tol, sc_lin)
        evaluation.stop()
    logging.info('evaluate_avg: done!')


classifier = SemanticClassifier(args.model)
model = classifier.model

if __name__ == '__main__':
    #update_most_similar_job_classes()
    evaluate_avg(classifier)
