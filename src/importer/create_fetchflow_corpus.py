# creates corpus of sentences from fetchflow data
import argparse
import os
import re

import psycopg2
from tqdm import tqdm

from src.preprocessing import preproc
from src.util.globals import CORPUS_DIR

parser = argparse.ArgumentParser(description="""Train Structural Classifier (NLTK)""")
args = parser.parse_args()

corpus_file = os.path.join(CORPUS_DIR, 'fetchflow.corpus')
if os.path.exists(corpus_file):
    os.remove(corpus_file)

with open(corpus_file, 'a', encoding='utf-8') as corpus, \
        psycopg2.connect(host='127.0.0.1', user='postgres', password='postgres', dbname='x28') as conn:
    # con't use ORM here because iterating over the whole table will result in a MemoryError!
    cursor = conn.cursor()
    cursor.execute("""SELECT count(*) AS count FROM fetchflow_html""")
    count = cursor.fetchone()[0]
    cursor.execute("""SELECT plaintext FROM fetchflow_html""")

    for row in tqdm(cursor, total=count, unit=' rows'):
        plaintext = row[0]
        paragraphs = plaintext.split('\n')
        for para in paragraphs:
            sentences = preproc.to_sentences(para)
            for sent in (sent.strip() for sent in sentences if sent.strip()[-1] in ['.', '?', '!']):
                words = preproc.to_words(sent)
                words = [x for x in words if x not in preproc.punctuation_tokens]
                words = [re.sub('[{}]'.format(preproc.punctuation), '', x) for x in words]
                if len(words) > 3:
                    line = ' '.join(word for word in words)
                    preproc.remove_special_chars(line)
                    corpus.write(line + '\n')
