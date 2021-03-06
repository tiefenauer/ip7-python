import unittest

from hamcrest import assert_that, is_

from src.scoring.loe_scorer_tolerant import TolerantLoeScorer

testee = TolerantLoeScorer()


class TestTolerantLoeScorer(unittest.TestCase):

    def test_calculate_similarity_without_matchin_items_returns_zero(self):
        assert_that(testee.calculate_similarity((80, 100), (40, 40)), is_(0))

    def test_calculate_similarity_with_matchin_items_returns_zero(self):
        assert_that(testee.calculate_similarity((80, 100), (80, 90)), is_(1))
        assert_that(testee.calculate_similarity((80, 100), (40, 100)), is_(1))
        assert_that(testee.calculate_similarity((80, 100), (80, 100)), is_(1))
