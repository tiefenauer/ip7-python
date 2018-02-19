import argparse
import logging
import os
import pickle

from tqdm import tqdm

from src.classifier.jobtitle.jobtitle_classifier_structural import JobtitleStructuralClassifier
from src.database.classification_results import StructuralClassificationResults
from src.database.test_data_x28 import X28TestData
from src.scoring.jobtitle_scorer_linear import LinearJobtitleScorer
from src.scoring.jobtitle_scorer_strict import StrictJobtitleScorer
from src.scoring.jobtitle_scorer_tolerant import TolerantJobtitleScorer
from src.util.globals import RESOURCE_DIR
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""Classifies data using structural approach (nouns/verbs + HTML-Tag)""")
parser.add_argument('model', nargs='?', help='file with saved model to evaluate')
parser.add_argument('id', nargs='?', type=int)
parser.add_argument('-s', '--split', nargs='?', type=float, default=0.8,
                    help='(optional) fraction value of labeled data to use for training/testing')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")

args = parser.parse_args()

if not args.model:
    # args.model = 'structural_model.gz' # old Naive Bayes
    args.model = 'multinomial.nb'

model_path = os.path.join(RESOURCE_DIR, args.model)
vectorizer_path = os.path.join(RESOURCE_DIR, 'tfidf.vectorizer')
with open(model_path, 'rb') as model_file, open(vectorizer_path, 'rb') as vectorizer_file:
    model = pickle.load(model_file)
    vectorizer = pickle.load(vectorizer_file)

classifier = JobtitleStructuralClassifier(model, vectorizer)
results = StructuralClassificationResults()

scorer_strict = StrictJobtitleScorer()
scorer_linear = LinearJobtitleScorer()
scorer_tolerant = TolerantJobtitleScorer()

results.truncate()

batch = []


def evaluate_batch(batch):
    predictions = classifier.predict_batch(batch)
    for prediction, row in zip(predictions, batch):
        score_strict = scorer_strict.calculate_score(row.title, prediction)
        score_linear = scorer_linear.calculate_score(row.title, prediction)
        score_tolerant = scorer_tolerant.calculate_score(row.title, prediction)
        scores = [score_strict, score_tolerant, score_linear]
        results.update_classification(row, prediction, scores)


for row in tqdm(X28TestData(args)):
    batch.append(row)
    if len(batch) == 1000:
        evaluate_batch(batch)
        batch = []

# last rows
evaluate_batch(batch)
