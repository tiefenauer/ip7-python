import collections
import unittest

from hamcrest import assert_that, is_, greater_than

from src.dataimport.known_jobs import KnownJobs


class TestKnownJobs(unittest.TestCase):
    def test_is_singleton(self):
        # arrange/act
        testee1 = KnownJobs()
        testee2 = KnownJobs()

        assert_that(testee1, is_(testee2))
        assert_that(testee1 == testee2, is_(True))

    def test_JobNameImporter_is_iterable(self):
        # arrange
        testee = KnownJobs()
        # act/assert
        assert_that(isinstance(testee, collections.Iterable), is_(True))
        assert_that(len(list(testee)), is_(greater_than(0)))
        # assert twice to make sure testee is non-exhaustable
        assert_that(len(list(testee)), is_(greater_than(0)))
