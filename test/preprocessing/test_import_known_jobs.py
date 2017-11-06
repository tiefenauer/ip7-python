import itertools
import unittest

from hamcrest import is_, assert_that, contains_inanyorder, empty

from src.preprocessing import collect_known_jobs as testee
from src.util import jobtitle_util


class TestImportJobNames(unittest.TestCase):
    def test_merge_both_same_returns_actual(self):
        # arrange
        actual = 'Trockenbauer'
        prediction = 'Trockenbauer'
        # act
        result = testee.merge(actual, prediction)
        assert_that(result, contains_inanyorder(actual))

    def test_merge_removes_leading_trailing_special_chars(self):
        assert_that(testee.merge('Bauphysiker ', 'Bauphysiker'), contains_inanyorder('Bauphysiker'))
        assert_that(testee.merge('Bauphysiker /', 'Bauphysiker'), contains_inanyorder('Bauphysiker'))

    def test_merge_different_forms_returns_male_form(self):
        job_name = 'Maler'
        for actual, prediction in itertools.combinations(jobtitle_util.create_variants(job_name), 2):
            message = '{} / {} should be merged to {}'.format(actual, prediction, job_name)
            assert_that(testee.merge(actual, prediction), contains_inanyorder(job_name), message)

    def test_merge_slashed_form_returns_multiple_jobs(self):
        assert_that(testee.merge('Maurer/Maurerin', 'Maurer'), contains_inanyorder('Maurer'))
        assert_that(testee.merge('Maurer/Polymechaniker', 'Maurer'), contains_inanyorder('Maurer', 'Polymechaniker'))
        assert_that(testee.merge('MaurerIn/Polymechaniker/-in', 'Maurer'), contains_inanyorder('Maurer', 'Polymechaniker'))

    def test_merge_partial_match_returns_full(self):
        assert_that(testee.merge('Möbelschreiner', 'Schreiner'), contains_inanyorder('Möbelschreiner'))
        assert_that(testee.merge('Bauspengler', 'Spengler'), contains_inanyorder('Bauspengler'))

    def test_marge_no_match_actual_is_known_job_returns_actual(self):
        actual_job_name = 'Polymechaniker'
        predicted_job_name = 'Elektroniker'
        polymechaniker_variants = jobtitle_util.create_variants(actual_job_name)
        elektroniker_variants = jobtitle_util.create_variants(predicted_job_name)

        for actual_variant, prediction_variant in zip(polymechaniker_variants, elektroniker_variants):
            assert_that(testee.merge(actual_variant, prediction_variant), contains_inanyorder(actual_job_name))

    def test_merge_no_match_actual_is_one_word_returns_actual(self):
        assert_that(testee.merge('Fassadenisolateur', 'Gipser'), contains_inanyorder('Fassadenisolateur'))
        assert_that(testee.merge('Fassadenisolateur (m/w)', 'Gipser'), contains_inanyorder('Fassadenisolateur'))

    def test_merge_no_match_actual_is_compound_word_returns_actual(self):
        assert_that(testee.merge('Kupfer-Spleisser', 'Monteur'), contains_inanyorder('Kupfer-Spleisser'))

    def test_merge_no_match_unmergeable_returns_None(self):
        assert_that(testee.merge('Projektleiter Sanitär', 'Techniker'), is_(empty()))
