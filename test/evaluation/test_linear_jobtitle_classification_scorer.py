import unittest

from hamcrest import *

from src.evaluation.jobtitle.jobtitle_classification_scorer_linear import LinearJobtitleClassificationScorer

testee = LinearJobtitleClassificationScorer()


class TestLinearJobtitleClassificationScorer(unittest.TestCase):

    def test_calculate_similarity_full_match_returns_one(self):
        # arrange/act/assert
        assert_that(testee.calculate_similarity('Polymechaniker', 'Polymechaniker'), is_(1))
        assert_that(testee.calculate_similarity('Senior System Engineer', 'Senior System Engineer'), is_(1))

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

    def test_calculate_similarity_simple_returns_correct_score(self):
        # arrange/act
        result = testee.calculate_similarity('Schichtleiter Maschinenbau', 'Schichtleiter')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_similarity_complex_returns_correct_score(self):
        # arrange/act
        result = testee.calculate_similarity('Lehrstelle als Logistiker/in (Distribution) EFZ', 'Lehrstelle Logistiker')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_similarity_ignores_stop_words(self):
        # arrange/act
        result = testee.calculate_similarity('Schichtleiter und Maschinenbau', 'Schichtleiter')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_similarity_ignores_gender_in(self):
        # arrange/act
        result = testee.calculate_similarity('Schichtleiter und Maschinenbau', 'Schichtleiterin')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_similarity_ignores_gender_euse(self):
        # arrange/act
        result = testee.calculate_similarity('Coiffeuse und Naildesignerin', 'Coiffeur')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_similarity_ignores_gender_frau(self):
        # arrange/act
        result = testee.calculate_similarity('Kauffrau und Chefin', 'Kauffrau')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_similarity_no_prediction_returns_zero(self):
        # arrange/act
        result = testee.calculate_similarity('Schichtleiter Maschinenbau', None)
        # assert
        assert_that(result, is_(0))

    def test_calculate_similarity_empty_prediction_returns_zero(self):
        # arrange/act
        result = testee.calculate_similarity('Schichtleiter Maschinenbau', '')
        # assert
        assert_that(result, is_(0))
