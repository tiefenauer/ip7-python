import unittest

from hamcrest import assert_that, only_contains

import src.preprocessing.create_job_classes as testee


class TestCreateJobClasses(unittest.TestCase):
    def test_create_write_variants_normal_job_returns_normal_job(self):
        # arrange
        job_name = 'Monteur'
        # act
        result = testee.create_write_variants(job_name)
        # assert
        assert_that(result, only_contains('Monteur'))

    def test_create_write_variants_hyphenated_job_returns_all_write_variants(self):
        # arrange
        job_name = 'Tax-Manager'
        # act
        result = testee.create_write_variants(job_name)
        # assert
        assert_that(result, only_contains('Tax-Manager', 'Taxmanager', 'Tax Manager'))

    def test_create_write_variants_compound_job_returns_all_write_variants(self):
        # arrange
        job_name = 'Taxmanager'
        # act
        result = testee.create_write_variants(job_name)
        # assert
        assert_that(result, only_contains('Tax-Manager', 'Taxmanager', 'Tax Manager'))
