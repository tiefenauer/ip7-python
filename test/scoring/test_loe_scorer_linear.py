import unittest

from hamcrest import assert_that, is_

from src.scoring.los_scorer_linear import LinearLoeScorer

testee = LinearLoeScorer()


class TestLinearLoeScorer(unittest.TestCase):

    def test_calculate_similarity_without_matching_items_returns_zero(self):
        assert_that(testee.calculate_similarity((80, 100), (40, 40)), is_(0.0))
        assert_that(testee.calculate_similarity((80, 100), (100, 80)), is_(0.0))

    def test_calculate_similarity_returns_correct_fraction_of_matching_items(self):
        assert_that(testee.calculate_similarity((80, 100), (80, 80)), is_(0.5))
        assert_that(testee.calculate_similarity((80, 100), (100, 100)), is_(0.5))
        assert_that(testee.calculate_similarity((80, 100), (80, 100)), is_(1.0))
