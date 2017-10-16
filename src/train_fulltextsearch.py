import pandas

from src.job_importer import process_stream

_job_names = pandas.read_csv('../resource/tbfulljob_DE.csv', delimiter=';')
_job_names.columns = ['job_name']


def match_with_whitelist(dom, job_names=_job_names):
    dom_str = str(dom)
    for job_name in job_names:
        if job_name in dom_str:
            yield job_name


if __name__ == '__main__':
    process_stream(match_with_whitelist)
