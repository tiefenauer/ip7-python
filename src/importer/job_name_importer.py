import pandas


class JobNameImporter(object):
    def __init__(self):
        self.job_names = pandas.read_csv('../resource/job_titles.tsv', delimiter=';', names=['job_name'])

    def __iter__(self):
        for job_name in self.job_names['job_name']:
            yield job_name
