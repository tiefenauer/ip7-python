import unittest

from hamcrest import *

from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator

testee = TolerantJobtitleEvaluator()


class TestTolerantJobtitleEvaluator(unittest.TestCase):
    def test_calculate_score_with_predicted_None_returns_zero(self):
        assert_that(testee.calculate_score("foo bar", None), is_(0))

    def test_calculate_score_with_predicted_not_in_actual_returns_zero(self):
        assert_that(testee.calculate_score("foo bar", "baq"), is_(0))

    def test_calculate_score_with_predicted_in_actual_returns_one(self):
        assert_that(testee.calculate_score("foo bar", "bar"), is_(1))
