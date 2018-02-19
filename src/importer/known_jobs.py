import os

import pandas

from src.util.globals import RESOURCE_DIR
from src.util.singleton import Singleton


class KnownJobs(metaclass=Singleton):
    def __init__(self):
        path = os.path.join(RESOURCE_DIR, 'known_jobs.tsv')
        self.job_names = pandas.read_csv(path, delimiter=';', names=['job_name'])

    def __iter__(self):
        for job_name in self.job_names['job_name']:
            yield job_name
