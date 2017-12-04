import os
import pandas


class KnownJobs(object):
    def __init__(self):
        path = os.path.abspath('D:/code/ip7-python/resource/known_jobs.tsv')
        self.job_names = pandas.read_csv(path, delimiter=';', names=['job_name'])

    def __iter__(self):
        for job_name in self.job_names['job_name']:
            yield job_name
