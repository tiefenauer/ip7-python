import collections
import unittest

from hamcrest import assert_that, instance_of, is_, not_, empty, greater_than

from src.provider.job_class_provider import JobClassProvider


class TestJobClassProvider(unittest.TestCase):
    def test_is_iterable_and_closeable(self):
        with JobClassProvider() as testee:
            assert_that(testee, is_(instance_of(collections.Iterable)))
            assert_that(len(list(testee)), is_(greater_than(0)))
            for item in testee:
                assert_that(item['id'], is_(not_(empty())))
                assert_that(item['job_class'], is_(not_(empty())))
                assert_that(item['job_class_stem'], is_(not_(empty())))

    def test_get_job_class_by_name_returns_result(self):
        # arrange
        job_name = 'Monteur'
        # act
        with JobClassProvider() as  testee:
            item = testee.get_job_class_by_name(job_name)
        # assert
        assert_that(item['id'], is_(not_(empty())))
        assert_that(item['job_class'], is_(not_(empty())))
        assert_that(item['job_class_stem'], is_(not_(empty())))

    def test_provide_job_variants_by_name_returns_list(self):
        # arrange
        job_name = 'Monteur'
        # act
        with JobClassProvider() as testee:
            variants = testee.get_variants_by_name(job_name)
        # assert
        assert_that(variants, is_(not_(empty())))

    def test_provide_job_variants_by_id_returns_list(self):
        # arrange
        job_name = 'Monteur'
        # act
        with JobClassProvider() as testee:
            job_entry = testee.get_job_class_by_name(job_name)
            variants = testee.get_variants_by_id(job_entry['id'])
        # assert
        assert_that(variants, is_(not_(empty())))
