import argparse
import json
import logging

import sys

from tqdm import tqdm

from src.importer.x28_importer import X28Importer


logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser(description="""
Reads X28 JSON data from a directory into a local postgres database. Only the most important attributes are read.
""")
parser.add_argument('-t', '--truncate', action='store_true',
                    help='truncate target tables before extraction (default=True)')
args = parser.parse_args()


if __name__ == '__main__':
    with X28Importer() as x28_importer:
        if args.truncate:
            x28_importer.truncate_tables()
        for text in tqdm(x28_importer, total=x28_importer.num_files, unit=' files'):
            x28_importer.insert(json.loads(text))