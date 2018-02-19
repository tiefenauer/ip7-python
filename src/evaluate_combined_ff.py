"""
Evaluates the combined approach on Fetchflow-Vacancies that
"""
import argparse
import logging
import os

import pandas

from src.classifier.jobtitle.jobtitle_classifier_combined import CombinedJobtitleClassifier
from src.classifier.loe.loe_classifier import LoeClassifier
from src.database.fetchflow_data import FetchflowData
from src.preprocessing.loe_preprocessor import LoePreprocessor
from src.preprocessing.sentence_preprocessor import SentencePreprocessor
from src.scoring.jobtitle_scorer_linear import LinearJobtitleScorer
from src.scoring.jobtitle_scorer_strict import StrictJobtitleScorer
from src.scoring.jobtitle_scorer_tolerant import TolerantJobtitleScorer
from src.scoring.loe_scorer_linear import LinearLoeScorer
from src.scoring.loe_scorer_strict import StrictLoeScorer
from src.scoring.loe_scorer_tolerant import TolerantLoeScorer
from src.util.globals import RESOURCE_DIR
from src.util.log_util import log_setup

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-c', '--calculate_score', type=bool, default=True,
                    help=""""(optional) calculate score on-the-fly. If set to False processing might be a bit faster 
                    but score will need to calculated manually afterwards (default: True)""")
parser.add_argument('-i', '--include_title', type=bool, default=True,
                    help='(optional) include title tag in evaluation. Default: True')
parser.add_argument('-s', '--split', nargs='?', type=float, default=1.0,
                    help='(optional) fraction value of labeled data to use for training')
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=False)')
parser.add_argument('-v', '--visualize', action='store_true',
                    help='(optional) visualize process by showing a live preview (default=False)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

log_setup()
log = logging.getLogger(__name__)

evaluation_file = os.path.join(RESOURCE_DIR, 'fetchflow_evaluation.xlsx')


def make_jobtitel_predictions():
    i = 0
    sentence_preprocessor = SentencePreprocessor()
    classifier = CombinedJobtitleClassifier()

    for row in FetchflowData():
        processed_data = sentence_preprocessor.preprocess_single(row)
        prediction = classifier.predict_class(processed_data)
        print('{}\t{}\t{}'.format(row.id, row.fetchflow_id, prediction))
        i += 1
        if i == 100:
            break


def make_loe_predictions():
    loe_preprocessor = LoePreprocessor()
    classifier = LoeClassifier()
    for row in FetchflowData():
        processed_data = loe_preprocessor.preprocess_single(row)
        workquota_min, workquota_max = classifier.predict_class(processed_data)
        print('{}\t{}\t{}\t{}'.format(row.id, row.fetchflow_id, workquota_min, workquota_max))


if __name__ == '__main__':
    # uncomment the following line to print jobtitle predictions for the first 100 vacancies to the console
    # make_jobtitel_predictions()

    # uncomment the following line to print LOE predictions for the first 100 vacancies to the console
    # make_loe_predictions()

    jt_scorer_strict = StrictJobtitleScorer()
    jt_scorer_linear = LinearJobtitleScorer()
    jt_scorer_tolerant = TolerantJobtitleScorer()
    loe_scorer_strict = StrictLoeScorer()
    loe_scorer_linear = LinearLoeScorer()
    loe_scorer_tolerant = TolerantLoeScorer()

    df = pandas.read_excel(evaluation_file, header=0, index_col=0)
    for index, row in df.iterrows():
        jt_actual = row['jobtitle_actual']
        jt_prediction = row['jobtitle_predicted']

        jt_score_strict = jt_scorer_strict.calculate_score(jt_actual, jt_prediction)
        jt_score_linear = jt_scorer_linear.calculate_score(jt_actual, jt_prediction)
        jt_score_tolerant = jt_scorer_tolerant.calculate_score(jt_actual, jt_prediction)

        row['score_strict'] = jt_score_strict
        row['score_linear'] = jt_score_linear
        row['score_tolerant'] = jt_score_tolerant

        loe_actual = (row['loe_min_actual'], row['loe_max_actual'])
        loe_prediction = (row['loe_min_predicted'], row['loe_max_predicted'])

        loe_score_strict = loe_scorer_strict.calculate_score(loe_actual, loe_prediction)
        loe_score_linear = loe_scorer_strict.calculate_score(loe_actual, loe_prediction)
        loe_score_tolerant = loe_scorer_strict.calculate_score(loe_actual, loe_prediction)

        print('{}\t{}\t{}\t\t{}\t{}\t{}\t'.format(jt_score_strict, jt_score_linear, jt_score_tolerant, loe_score_strict,
                                                  loe_score_linear, loe_score_tolerant))
