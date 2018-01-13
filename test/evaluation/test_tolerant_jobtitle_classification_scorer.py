import unittest

from hamcrest import *

from src.evaluation.jobtitle.jobtitle_classification_scorer_tolerant import TolerantJobtitleClassificationScorer

testee = TolerantJobtitleClassificationScorer()


class TestTolerantJobtitleClassificationScorer(unittest.TestCase):
    def test_calculate_similarity_without_prediction_returns_zero(self):
        assert_that(testee.calculate_similarity("foo bar", None), is_(0))

    def test_calculate_similarity_with_empty_prediction_returns_zero(self):
        assert_that(testee.calculate_similarity("foo bar", ''), is_(0))

    def test_calculate_similarity_with_predicted_not_in_actual_returns_zero(self):
        assert_that(testee.calculate_similarity("foo bar", "baq"), is_(0))

    def test_calculate_similarity_with_predicted_in_actual_returns_one(self):
        assert_that(testee.calculate_similarity("foo bar", "bar"), is_(1))

    def test_calculate_similarity_full_match_ignores_mw_forms(self):
        # arrange/act/asser
        assert_that(testee.calculate_similarity('Senior System Engineer (m/w)', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer   (m/w)', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer m/w', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer   m/w', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer mw', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer   mw', 'Senior System Engineer'), is_(1))

    def test_calculate_similarity_full_match_ignores_percentages(self):
        # arrange/act/asser
        assert_that(testee.calculate_similarity('Senior System Engineer 100%', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer   100%', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer 60%', 'Senior System Engineer'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer   60%', 'Senior System Engineer'), is_(1))

    def test_calculate_similarity_full_match_ignores_gender(self):
        # arrange/act/assert
        assert_that(testee.calculate_similarity('MalerIn', 'Maler'), is_(1))
        assert_that(testee.calculate_similarity('Maler/in', 'Maler'), is_(1))
        assert_that(testee.calculate_similarity('Maler/-in', 'Maler'), is_(1))
        assert_that(testee.calculate_similarity('Maler(in)', 'Maler'), is_(1))
        assert_that(testee.calculate_similarity('Maler', 'MalerIn'), is_(1))
        assert_that(testee.calculate_similarity('Maler', 'Maler/in'), is_(1))
        assert_that(testee.calculate_similarity('Maler', 'Maler/-in'), is_(1))
        assert_that(testee.calculate_similarity('Maler', 'Maler(in)'), is_(1))
        assert_that(testee.calculate_similarity('MalerIn', 'Maler/-in'), is_(1))
        assert_that(testee.calculate_similarity('Maler/in', 'Maler/-in'), is_(1))
        assert_that(testee.calculate_similarity('Maler/-in', 'MalerIn'), is_(1))
        assert_that(testee.calculate_similarity('Maler(in)', 'Maler'), is_(1))

    def test_calculate_similarity_with_multiple_words_returns_one(self):
        assert_that(testee.calculate_similarity('Projekt Ingenieur (m/w)', 'Projekt Ingenieur'), is_(1))
