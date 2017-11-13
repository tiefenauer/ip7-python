import collections
import unittest

from hamcrest import assert_that, instance_of, is_, not_, empty, greater_than

from src.database.job_classes import JobClasses


class TestJobClasses(unittest.TestCase):
    def test_is_iterable_and_closeable(self):
        with JobClasses() as testee:
            assert_that(testee, is_(instance_of(collections.Iterable)))
            assert_that(len(list(testee)), is_(greater_than(0)))
            for item in testee:
                assert_that(item['id'], is_(not_(empty())))
                assert_that(item['job_name'], is_(not_(empty())))
                assert_that(item['job_name_stem'], is_(not_(empty())))
