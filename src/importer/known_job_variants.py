from src.importer.known_jobs import KnownJobs
from src.util import jobtitle_util
from src.util.singleton import Singleton


class KnownJobVariants(metaclass=Singleton):
    """Singleton for all job names and their variants"""

    def __init__(self):
        self.known_job_variants = [(job_name, jobtitle_util.create_variants(job_name)) for job_name in KnownJobs()]

    def __iter__(self):
        for job_name, variants in self.known_job_variants:
            yield job_name, variants
