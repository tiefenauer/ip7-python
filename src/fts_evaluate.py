import argparse
import logging
import sys

from tqdm import tqdm

from src import preproc
from src.classifier.jobtitle_count_based import CountBasedJobTitleClassification
from src.classifier.jobtitle_feature_based import FeatureBasedJobTitleClassification
from src.classifier.jobtitle_title_based import TitleBasedJobTitleClassifier
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator
from src.importer.data_train import TrainingData
from src.util.boot_util import choose_classifier, choose_evaluation

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-e', '--evaluator', choices=['strict', 'tolerant', 'linear'],
                    help="""method to use to evaluate the predicted class. 
                    - 'strict': {}
                    - 'tolerant': {}
                    - 'linear': {}
                    """.format(StrictEvaluator.DESCRIPTION,
                               TolerantJobtitleEvaluator.DESCRIPTION,
                               LinearJobTitleEvaluator.DESCRIPTION))
parser.add_argument('-s', '--strategy', choices=['count', 'feature-based', 'title-based'], default='feature-based',
                    help="""strategy used for classification:
                    - 'count': {}
                    - 'feature-based': {}
                    - 'title-based': {}
                    """.format(CountBasedJobTitleClassification.DESCRIPTION,
                               FeatureBasedJobTitleClassification.DESCRIPTION,
                               TitleBasedJobTitleClassifier.DESCRIPTION
                               ))
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=True). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
args = parser.parse_args()

classifier = choose_classifier(args)
evaluation = choose_evaluation(args, classifier)

if __name__ == '__main__':
    with TrainingData(args.id) as data_train:
        if args.write and args.truncate:
            data_train.truncate_target()
        logging.info("Processing {} rows...".format(data_train.num_rows))
        i = 0
        for row in (row for row in tqdm(data_train, total=data_train.num_rows, unit=' rows') if row['html']):
            i += 1
            relevant_tags = preproc.preprocess(row['html'])
            job_title = classifier.classify(relevant_tags)
            score_strict, score_tolerant, score_linear = evaluation.update(row['title'], job_title, i, data_train.num_rows)
            if job_title is not None:
                if args.write:
                    data_train.classify_job(row['id'], job_title, score_strict, score_tolerant, score_linear)
        evaluation.stop()
