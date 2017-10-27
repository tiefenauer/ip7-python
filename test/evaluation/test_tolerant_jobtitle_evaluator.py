import unittest

from hamcrest import *

from src.evaluation.tolerant_jobtitle_evaluator import TolerantJobtitleEvaluator

testee = TolerantJobtitleEvaluator()


class TestTolerantJobtitleEvaluator(unittest.TestCase):
    def test_evaluate_with_predicted_None_returns_false(self):
        assert_that(testee.features_match("foo bar", None), is_(False))

    def test_evaluate_with_predicted_not_in_actual_returns_false(self):
        assert_that(testee.features_match("foo bar", "baq"), is_(False))

    def test_evaluate_with_predicted_in_actual_returns_false(self):
        assert_that(testee.features_match("foo bar", "bar"), is_(True))
