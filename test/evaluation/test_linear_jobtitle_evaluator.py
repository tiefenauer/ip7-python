import unittest

from hamcrest import *

from src.evaluation.scorer_jobtitle_linear import LinearJobTitleScorer

testee = LinearJobTitleScorer(0.7)


class TestLinearJobTitleEvaluator(unittest.TestCase):
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
