import argparse
import logging

from sklearn.ensemble import RandomForestClassifier

from src.classifier.jobtitle.jobtitle_semantic_classifier_rf import JobtitleSemanticClassifierRF
from src.database.X28TestData import X28TestData
from src.database.X28TrainData import X28TrainData
from src.evaluation.jobtitle.evaluator_jobtitle_semantic_rf import SemanticRFEvaluation
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using semantic approach (Word2Vec)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate_avg')
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")

args = parser.parse_args()

data_dir = 'D:/code/ip7-python/resource/models/word2vec'

if not args.model:
    args.model = '2017-11-21-12-38-54_300features_40minwords_10context.gz'

args.split = 0.001
data_train = X28TrainData(args)
args.split = 0.999
data_test = X28TestData(args)

preprocessor = SemanticPreprocessor(remove_stopwords=True)  # remove stopwords for evaluation
classifier = JobtitleSemanticClassifierRF(args, preprocessor)
evaluation = SemanticRFEvaluation(args, classifier)

if __name__ == '__main__':
    processed_train_data = preprocessor.preprocess(data_train, data_train._count)
    processed_test_data = preprocessor.preprocess(data_test, data_test._count)
    trainDataVecs = classifier.create_average_vectors(processed_train_data, data_train._count)
    testDataVecs = classifier.create_average_vectors(processed_test_data, data_test._count)
    args.split = 0.001
    trainDataLabels = [row.title for row in X28TrainData(args)]
    args.split = 0.999
    testDataLabels = [row.title for row in X28TestData(args)]

    forest = RandomForestClassifier(n_estimators=100)
    forest.fit(trainDataVecs, trainDataLabels)

    result = forest.predict(testDataVecs)
    log.info('evaluate_rf: evaluating random forest...')
    args.split = 0.999
    data_test = X28TestData(args)
    processed_test_data = preprocessor.preprocess(data_test, data_test._count)
    for i, (row, predicted_class) in enumerate(zip(processed_test_data, result), 1):
        sc_str, sc_tol, sc_lin = evaluation.update(row.title, predicted_class, i, data_test._count)
        results.update_classification(row, predicted_class, sc_str, sc_tol, sc_lin)

    # log.info('evaluate_avg: evaluating Semantic Classifier by averaging vectors...')
    # for i, row in enumerate(processed_test_data, 1):
    #     predicted_class = classifier.classify(row.processed)
    #     sc_str, sc_tol, sc_lin = evaluation.update(row.title, predicted_class, i, data_test.count)
    #     results.update_classification(row, predicted_class, sc_str, sc_tol, sc_lin)
    evaluation.stop()
    log.info('evaluate_avg: done!')
