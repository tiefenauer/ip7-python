from src import db
from src.db import Database
import csv
import re
import gensim
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from difflib import SequenceMatcher

stemmer = SnowballStemmer('german', ignore_stopwords=True)
stopwords_de = stopwords.words('german')

RESOURCES_PATH = '../../resource/'

# matches all (...), [...] and {...}
brackets = r"\[([^\]]+)]|\(([^)]+)\)|{([^}]+)}"
female = r"(\/-?in)|(\/-?euse)|(\/-?frau)"


def create_training_data():
    jobs = create_job_map()
    conn = db.connectTo(Database.FETCHFLOW)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT count(*) as num_total FROM labeled_text")
    num_total = cursor.fetchone()['num_total']
    cursor.execute("SELECT count(*) as num_trained FROM labeled_text WHERE has_job_title = 1")
    num_trained = cursor.fetchone()['num_trained']
    cursor.execute("SELECT count(*) as num_untrained FROM labeled_text WHERE has_job_title = 0")
    num_untrained = cursor.fetchone()['num_untrained']
    batchsize = 1000
    for i in range(0, num_untrained, batchsize):
        cursor.execute("SELECT * FROM labeled_text WHERE has_job_title = 0 LIMIT %s OFFSET %s", (batchsize, batchsize))
        for record in cursor:
            job_titles = find_matching_job_titles(record['title'], jobs)
            print(job_titles)


def create_job_map():
    jobs = import_jobs('branches.csv')
    # for job in jobs: print(job)
    job_map = [{'original': job, 'uncluttered': job_uncluttered, 'stem': stemmer.stem(job_uncluttered)}
               for (job, job_uncluttered) in ((job, ' '.join(strip_clutter(job))) for job in jobs)]
    return job_map


def find_matching_job_titles(titles, jobs):
    results = set()
    a = [1,2,3,4,5]
    b = [9,8,7,7,6]
    res = set(a) & set(b)
    titles = strip_clutter(titles)
    for job, job_uncluttered, stems in jobs:
        for stem in stems.split(' '):
            for title in titles:
                if similarity(title, stem) > 0.8:
                    results.add(job)
        # results.update(set(titles) & set(stems.split(' ')))
    return results

def similarity(a,b):
    return SequenceMatcher(None,a,b).ratio()

def strip_clutter(str):
    stripped = re.sub(brackets, '', str)
    stripped = re.sub(female, '', str)
    return [word for word in stripped.split(' ') if word not in stopwords_de]


def import_jobs(filename):
    lines = open_file(filename)
    return (job for job in (line[2] for line in lines))


def open_file(filename, delimiter=';'):
    with open(RESOURCES_PATH + filename, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=delimiter)
        for row in rows:
            yield row


create_training_data()
