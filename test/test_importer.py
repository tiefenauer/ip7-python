import collections
import unittest

from pytest import fail

from src.importer import JobNameImporter


class TestImporter(unittest.TestCase):

    def test_JobNameImporter_is_iterable(self):
        # arrange
        job_importer = JobNameImporter()
        # act/assert
        if not isinstance(job_importer, collections.Iterable):
            fail('JobNameImporter is not iterable!')