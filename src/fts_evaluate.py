import argparse
import logging
import sys

from tqdm import tqdm

from src import preproc
from src.classifier import classifier_jobtitle
from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator
from src.evaluation.strict_evaluator import StrictEvaluator
from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator
from src.importer.data_train import TrainingData

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-e', '--evaluator', choices=['strict', 'tolerant', 'linear'], default='tolerant',
                    help="""method to use to evaluate the predicted class.\ 
                    - 'strict': {}
                    - 'tolerant': {}
                    - 'linear': {}
                    """.format(StrictEvaluator.DESCRIPTION, TolerantJobtitleEvaluator.DESCRIPTION, LinearJobTitleEvaluator.DESCRIPTION))
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=False). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")

args = parser.parse_args()

evaluator = TolerantJobtitleEvaluator()
if args.evaluator == 'strict':
    evaluator = StrictEvaluator()
logging.info("description of evaluation: " + evaluator.describe_evaluation())

if __name__ == '__main__':
    with TrainingData(args.id) as data_train:
        if args.truncate:
            data_train.truncate_classification_tables()
        logging.info("Processing {} rows...".format(data_train.num_rows))
        tqdm_data = tqdm(data_train, total=data_train.num_rows, unit=' rows')
        for row in (row for row in tqdm_data if row['html']):
            relevant_tags = preproc.preprocess(row['html'])
            # (job_title, job_count) = classifier_jobtitle.find_best(relevant_tags)
            (job_title, job_count, job_score) = classifier_jobtitle.classify(relevant_tags)
            evaluator.evaluate(row['title'], job_title)
            if job_title is not None:
                tqdm_data.set_description(evaluator.get_description())
                if args.write:
                    data_train.classify_job(row['id'], job_title, job_count)
