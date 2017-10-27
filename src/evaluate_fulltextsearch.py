import argparse
import logging
import sys

from tqdm import tqdm

from src import preproc
from src.classifier import classifier_jobtitle
from src.importer.data_train import TrainingData

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads training data and classifies it using full text search.
""")
parser.add_argument('-w', '--write', action='store_false',
                    help="""Write classification results to DB (default=False). If set to true this will save the 
                    classification results in the DB. If set to false this script will only provide a live view
                    on the classifier's performance""")
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
args = parser.parse_args()


def evaluate_live(positives, negatives, actual_job_title, predicted_job_title):
    if actual_job_title == predicted_job_title:
        positives += 1
    else:
        negatives += 1
    perf = positives / (positives + negatives)
    return positives, negatives, perf


if __name__ == '__main__':
    with TrainingData() as data_train:
        if args.truncate:
            data_train.truncate_classification_tables()
        logging.info("Processing {} rows...".format(data_train.num_rows))
        positives = 0
        negatives = 0
        performance = 0
        tqdm_data = tqdm(data_train, total=data_train.num_rows, unit=' rows')
        for row in (row for row in tqdm_data if row['html']):
            relevant_tags = preproc.preprocess(row['html'])
            (job_title, job_count) = classifier_jobtitle.find_best(relevant_tags)
            if job_title is not None:
                (positives, negatives, performance) = evaluate_live(positives, negatives, row['title'], job_title)
                desc = "positives={}, negatives={}, performance={}".format(positives, negatives, "{:1.4f}".format(performance))
                tqdm_data.set_description(desc)
                if args.write:
                    data_train.classify_job(row['id'], job_title, job_count)
