import collections
import unittest

from hamcrest import assert_that, is_, greater_than

from src.dataimport.known_jobs import KnownJobs


class TestJobNameImporter(unittest.TestCase):
    def test_JobNameImporter_is_iterable(self):
        # arrange
        testee = KnownJobs()
        # act/assert
        assert_that(isinstance(testee, collections.Iterable), is_(True))
        assert_that(len(list(testee)), is_(greater_than(0)))
