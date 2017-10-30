import unittest

from hamcrest import *

from src.evaluation.linear_jobtitle_evaluator import LinearJobTitleEvaluator

testee = LinearJobTitleEvaluator(0.7)


class TestLinearJobTitleEvaluator(unittest.TestCase):
    def test_calculate_score_simple_returns_correct_score(self):
        # arrange/act
        result = testee.calculate_score('Schichtleiter Maschinenbau', 'Schichtleiter')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_score_complex_returns_correct_score(self):
        # arrange/act
        result = testee.calculate_score('Lehrstelle als Logistiker/in (Distribution) EFZ', 'Lehrstelle Logistiker')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_score_ignores_stop_words(self):
        # arrange/act
        result = testee.calculate_score('Schichtleiter und Maschinenbau', 'Schichtleiter')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_score_ignores_gender_in(self):
        # arrange/act
        result = testee.calculate_score('Schichtleiter und Maschinenbau', 'Schichtleiterin')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_score_ignores_gender_euse(self):
        # arrange/act
        result = testee.calculate_score('Coiffeuse und Naildesignerin', 'Coiffeur')
        # assert
        assert_that(result, is_(0.5))

    def test_calculate_score_ignores_gender_frau(self):
        # arrange/act
        result = testee.calculate_score('Kauffrau und Chefin', 'Kauffrau')
        # assert
        assert_that(result, is_(0.5))