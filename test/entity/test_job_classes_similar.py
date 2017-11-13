import collections
import unittest

from hamcrest import assert_that, instance_of, is_

from src.database.job_classes_similar import JobClassesSimilar


class TestJobClassesSimilar(unittest.TestCase):
    def test_is_iterable_and_closeable(self):
        with JobClassesSimilar() as testee:
            assert_that(testee, is_(instance_of(collections.Iterable)))
