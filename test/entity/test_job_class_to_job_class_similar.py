import collections
import unittest

from hamcrest import assert_that, is_, instance_of

from src.entity.job_class_to_job_class_similar import JobClassToJobClassSimilar


class TestJobClassToJobClassSimilar(unittest.TestCase):
    def test_is_iterable_and_closeable(self):
        with JobClassToJobClassSimilar() as testee:
            assert_that(testee, is_(instance_of(collections.Iterable)))
