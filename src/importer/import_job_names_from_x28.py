import re

from tqdm import tqdm

from src.database.x28_data import X28Data
from src.importer.known_jobs import KnownJobs
from src.util.log_util import log_setup

log_setup()

resource_dir = 'D:/code/ip7-python/resource/'
known_jobs = sorted(set(KnownJobs()))

if __name__ == '__main__':
    i = 0
    for row in tqdm(X28Data()):
        i += 1
        if i == 10:
            break
        for job_name in known_jobs:
            p = re.compile(r'\b[^\s\/]+{}[^\s^\/]+\b'.format(re.escape(job_name)), re.IGNORECASE)
            for match in (match.title() for match in re.findall(p, row.title)):
                if match not in known_jobs:
                    known_jobs.append(match)
