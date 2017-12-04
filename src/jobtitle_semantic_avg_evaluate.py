import argparse
import logging

from pony.orm import commit, db_session
from tqdm import tqdm

from src.classifier.jobtitle.jobtitle_semantic_classifier_avg import JobtitleSemanticClassifierAvg
from src.database.X28TestData import X28TestData
from src.database.entities_pg import Job_Class, Job_Class_Similar, Job_Class_To_Job_Class_Similar
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from src.util.log_util import log_setup
from src.evaluation.jobtitle.evaluator_jobtitle_semantic_avg import SemanticAVGEvaluation

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate_avg')
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training/testing')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")

args = parser.parse_args()


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
    log.info('update_most_similar_job_classes: Updating DB with most similar jobs for trained jobs...')
    with db_session:
        # truncate previous mappings
        Job_Class_To_Job_Class_Similar.select().delete(bulk=True)
        Job_Class_Similar.select().delete(bulk=True)
        commit()
        # add new mappings
        known_and_trained_jobs = list(job_class for job_class in Job_Class.select()
                                      if job_class.job_name in model.index2word)

        for job_class in tqdm(known_and_trained_jobs, unit=' rows'):
            for similar_name, score in model.most_similar(job_class.job_name):
                if Job_Class_Similar.exists(job_name_similar=similar_name):
                    job_class_similar = Job_Class_Similar.get(job_name_similar=similar_name)
                else:
                    job_class_similar = Job_Class_Similar(job_name_similar=similar_name)
                commit()
                Job_Class_To_Job_Class_Similar(fk_job_class=job_class.id, fk_job_class_similar=job_class_similar.id,
                                               score=score)
    log.info('update_most_similar_job_classes: done!')


if not args.model:
    args.model = 'semantic_avg_2017-11-21-12-38-54_300features_40minwords_10context.gz'

preprocessor = SemanticPreprocessor(remove_stopwords=True)  # remove stopwords for evaluation
classifier = JobtitleSemanticClassifierAvg(args, preprocessor)
evaluation = SemanticAVGEvaluation(args, classifier)

if __name__ == '__main__':
    log.info('evaluate_avg: evaluating Semantic Classifier by averaging vectors...')
    data_test = X28TestData(args)
    evaluation.evaluate(data_test)
    evaluation.stop()
    log.info('evaluate_avg: done!')
