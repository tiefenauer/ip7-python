import argparse
import logging
import sys

from tqdm import tqdm

from src import preproc
from src.classifier import classifier_jobtitle
from src.evaluation.evaluate_tolerant import TolerantJobTitleClassificationEvaluator
from src.importer.data_train import TrainingData

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('id', nargs='?', type=int, help='(optional) single id to process')
parser.add_argument('-w', '--write', action='store_true',
                    help="""Write classification results to DB (default=False). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
args = parser.parse_args()


if __name__ == '__main__':
    evaluator = TolerantJobTitleClassificationEvaluator()
    with TrainingData(args.id) as data_train:
        if args.truncate:
            data_train.truncate_classification_tables()
        logging.info("Processing {} rows...".format(data_train.num_rows))
        tqdm_data = tqdm(data_train, total=data_train.num_rows, unit=' rows')
        for row in (row for row in tqdm_data if row['html']):
            relevant_tags = preproc.preprocess(row['html'])
            (job_title, job_count) = classifier_jobtitle.find_best(relevant_tags)
            evaluator.evaluate(row['title'], job_title)
            if job_title is not None:
                tqdm_data.set_description(evaluator.get_description())
                if args.write:
                    data_train.classify_job(row['id'], job_title, job_count)
