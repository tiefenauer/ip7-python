import collections
import unittest
from unittest.test.testmock.support import is_instance

from hamcrest import greater_than, assert_that, is_, instance_of

from src.dataimport.known_job_variants import KnownJobVariants


class TestKnownJobVariants(unittest.TestCase):

    def test_is_singleton(self):
        # arrange/act
        testee1 = KnownJobVariants()
        testee2 = KnownJobVariants()

        assert_that(testee1, is_(testee2))
        assert_that(testee1 == testee2, is_(True))

    def test_is_iterable(self):
        testee = KnownJobVariants()
        # act/assert
        assert_that(testee, instance_of(collections.Iterable))
        assert_that(len(list(testee)), is_(greater_than(0)))
        # assert twice to make sure testee is non-exhaustable
        assert_that(len(list(testee)), is_(greater_than(0)))

    def test_yields_mapping_tuples(self):
        for job_name, variant in KnownJobVariants():
            assert_that(is_instance(job_name, str))
            assert_that(is_instance(variant, str))
