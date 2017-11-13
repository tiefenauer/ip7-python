import argparse
import logging
import sys

from src.classifier.semantic_classifier import SemanticClassifier
from src.entity.job_class_to_job_class_similar import JobClassToJobClassSimilar
from src.entity.job_classes_similar import JobClassesSimilar
from src.evaluation.evaluation import Evaluation
from src.importer.data_train import TrainingData
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor
from src.entity.job_classes import JobClasses

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate')
parser.add_argument('-l', '--limit', nargs='?', type=float, default=1.0,
                    help='(optional) fraction of labeled data to use for training')
parser.add_argument('-o', '--offset', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to start from')
parser.add_argument('-m', '--model',
                    help='(optional) file with saved model to use. A new model will be created if not set.')
args = parser.parse_args()

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

preprocessor = SemanticX28Preprocessor()


def evaluate(clf):
    evaluation = Evaluation(clf)
    logging.info('evaluating model by matching predicted class with actual class for last 20% of labeled data')
    with TrainingData(args) as data_train:
        i = 0
        for actual_class, sentences in ((actual_class, sents) for (row_id, actual_class, sents) in
                                        preprocessor.preprocess(data_train)):
            i += 1
            predicted_class = clf.classify(sentences)
            evaluation.update(actual_class, predicted_class, i, data_train.num_rows)
        evaluation.stop()


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
    with JobClasses() as job_classes, JobClassToJobClassSimilar() as job_class_to_similar, JobClassesSimilar() as job_classes_similar:
        for job in (row['job_class'] for row in job_classes if row['job_class'] in model.index2word):
            for job_similar, score in model.most_similar(job):
                print(job, job_similar, score)


classifier = SemanticClassifier(args.model)
model = classifier.model

if __name__ == '__main__':
    update_most_similar_job_classes()
    doesnt_match('Monteur Coiffeur Bahn Manager')

    # evaluate(classifier)
