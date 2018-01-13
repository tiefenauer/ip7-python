import collections
import unittest

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
        for job_name, variants in KnownJobVariants():
            assert_that(job_name, is_(instance_of(str)))
            assert_that(variants, is_(instance_of(set)))
            for variant in variants:
                assert_that(variant, is_(instance_of(str)))
