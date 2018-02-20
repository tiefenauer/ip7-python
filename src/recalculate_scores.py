"""
recalculatae scores for classification results that are already written to the DB
"""
import argparse
import logging

from pony.orm import commit, db_session
from tqdm import tqdm

from src.database.entities_pg import Classification_Results
from src.scoring.jobtitle_scorer_linear import LinearJobtitleScorer
from src.scoring.jobtitle_scorer_strict import StrictJobtitleScorer
from src.scoring.jobtitle_scorer_tolerant import TolerantJobtitleScorer
from src.scoring.loe_scorer_linear import LinearLoeScorer
from src.scoring.loe_scorer_strict import StrictLoeScorer
from src.scoring.loe_scorer_tolerant import TolerantLoeScorer
from src.util.log_util import log_setup

log_setup()
log = logging.getLogger(__name__)

classification_methods = [
    'all',
    'jobtitle-fts',
    'jobtitle-combined',
    'jobtitle-semantic',
    'jobtitle-structural',
    'loe-fts'
]

parser = argparse.ArgumentParser(description="""
Re-calculates scores for classification results
""")
parser.add_argument('method', choices=classification_methods, type=str,
                    help='classification method for which the scores should be re-calculated')
args = parser.parse_args()

if __name__ == '__main__':
    clf_method = args.method
    if clf_method == 'loe-fts':
        scorer_linear = LinearLoeScorer()
        scorer_tolerant = TolerantLoeScorer()
        scorer_strict = StrictLoeScorer()
    else:
        scorer_linear = LinearJobtitleScorer()
        scorer_tolerant = TolerantJobtitleScorer()
        scorer_strict = StrictJobtitleScorer()

    with db_session:
        i = 0
        query = Classification_Results.select(lambda r: clf_method == 'all' or r.clf_method == clf_method)
        for row in tqdm(query, total=query.count(), unit=' rows'):
            if clf_method == 'loe-fts':
                actual_class = (row.x28_row.workquota_min, row.x28_row.workquota_max)
                predicted_class = (row.workquota_min, row.workquota_max)
            else:
                actual_class = row.x28_row.title
                predicted_class = row.job_name
            row.score_strict = scorer_strict.calculate_score(actual_class, predicted_class)
            row.score_tolerant = scorer_tolerant.calculate_score(actual_class, predicted_class)
            row.score_linear = scorer_linear.calculate_score(actual_class, predicted_class)
            commit()
