import argparse
import logging

from pony.orm import commit, db_session
from tqdm import tqdm

from src.database.entities_pg import Classification_Results
from src.evaluation.jobtitle.jobtitle_classification_scorer_linear import LinearJobtitleClassificationScorer
from src.evaluation.jobtitle.jobtitle_classification_scorer_strict import StrictJobtitleClassificationScorer
from src.evaluation.jobtitle.jobtitle_classification_scorer_tolerant import TolerantJobtitleClassificationScorer
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

classification_methods = [
    'all',
    'jobtitle-fts',
    'jobtitle-combined',
    'jobtitle-semantic-rf',
    'jobtitle-semantic-avg',
    'jobtitle-structural-nv',
    'jobtitle-structural-nvt',
    'loe-fts'
]

parser = argparse.ArgumentParser(description="""
Re-calculates scores for classification results
""")
parser.add_argument('method', choices=classification_methods, type=str,
                    help='(optional) classification method for which the scores should be re-calculated (default: all)')
args = parser.parse_args()

if __name__ == '__main__':
    clf_method = args.method
    scorer_linear = LinearJobtitleClassificationScorer()
    scorer_tolerant = TolerantJobtitleClassificationScorer()
    scorer_strict = StrictJobtitleClassificationScorer()

    with db_session:
        i = 0
        query = Classification_Results.select(lambda r: clf_method == 'all' or r.clf_method == clf_method)
        for row in tqdm(query, total=query.count(), unit=' rows'):
            actual_class = row.x28_row.title
            predicted_class = row.job_name
            row.score_strict = scorer_strict.calculate_score(actual_class, predicted_class)
            row.score_tolerant = scorer_tolerant.calculate_score(actual_class, predicted_class)
            row.score_linear = scorer_linear.calculate_score(actual_class, predicted_class)
            commit()
