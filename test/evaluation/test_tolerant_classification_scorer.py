import unittest

from hamcrest import *

from src.evaluation.classification_scorer_tolerant import TolerantClassificationScorer

testee = TolerantClassificationScorer()


class TestTolerantClassificationScorer(unittest.TestCase):
    def test_calculate_score_without_prediction_returns_zero(self):
        assert_that(testee.calculate_similarity("foo bar", None), is_(0))

    def test_calculate_score_with_empty_prediction_returns_zero(self):
        assert_that(testee.calculate_similarity("foo bar", ''), is_(0))

    def test_calculate_score_with_predicted_not_in_actual_returns_zero(self):
        assert_that(testee.calculate_similarity("foo bar", "baq"), is_(0))

    def test_calculate_score_with_predicted_in_actual_returns_one(self):
        assert_that(testee.calculate_similarity("foo bar", "bar"), is_(1))
