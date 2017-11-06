import itertools
import unittest

from hamcrest import is_, assert_that

from src.preprocessing import import_known_jobs as testee
from src.util import jobtitle_util


class TestImportJobNames(unittest.TestCase):
    def test_merge_both_same_returns_actual(self):
        # arrange
        actual = 'Trockenbauer'
        prediction = 'Trockenbauer'
        # act
        result = testee.merge(actual, prediction)
        assert_that(result, is_(actual))

    def test_merge_different_forms_returns_male_form(self):
        job_name = 'Maler'
        for actual, prediction in itertools.combinations(jobtitle_util.create_variants(job_name), 2):
            message = '{} / {} should be merged to {}'.format(actual, prediction, job_name)
            assert_that(testee.merge(actual, prediction), is_(job_name), message)

    @unittest.skip('kann ev. noch implementiert werden')
    def test_merge_slashed_form_returns_male_form(self):
        assert_that(testee.merge('Maurer/Maurerin', 'Maurer'), is_(('Maurer', 'predicted')))

    def test_merge_partial_match_returns_full(self):
        assert_that(testee.merge('Möbelschreiner', 'Schreiner'), is_('Möbelschreiner'))
        assert_that(testee.merge('Bauspengler', 'Spengler'), is_('Bauspengler'))

    def test_marge_no_match_actual_is_known_job_returns_actual(self):
        actual_job_name = 'Polymechaniker'
        predicted_job_name = 'Elektroniker'
        polymechaniker_variants = jobtitle_util.create_variants(actual_job_name)
        elektroniker_variants = jobtitle_util.create_variants(predicted_job_name)

        for actual_variant, prediction_variant in zip(polymechaniker_variants, elektroniker_variants):
            assert_that(testee.merge(actual_variant, prediction_variant), is_(actual_job_name))

    def test_merge_no_match_actual_is_one_word_returns_actual(self):
        assert_that(testee.merge('Fassadenisolateur', 'Gipser'), is_('Fassadenisolateur'))
        assert_that(testee.merge('Fassadenisolateur (m/w)', 'Gipser'), is_('Fassadenisolateur'))

    def test_merge_no_match_actual_is_compound_word_returns_actual(self):
        assert_that(testee.merge('Kupfer-Spleisser', 'Monteur'), is_('Kupfer-Spleisser'))

    def test_merge_no_match_unmergeable_returns_None(self):
        assert_that(testee.merge('Projektleiter Sanitär', 'Techniker'), is_(None))
