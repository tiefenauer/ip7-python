import argparse
import json
import logging
import sys

from tqdm import tqdm

from src.importer.x28_json_importer import X28JsonImporter

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads X28 JSON data from a directory into a local postgres database. Only the most important attributes are read.
""")
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
args = parser.parse_args()

if __name__ == '__main__':
    with X28JsonImporter() as data_train_importer:
        if args.truncate:
            data_train_importer.truncate_tables()
        for text in tqdm(data_train_importer, total=data_train_importer.num_files, unit=' files'):
            data_train_importer.insert(json.loads(text))
