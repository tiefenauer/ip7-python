import unittest

from hamcrest import *

from src.classifier import jobtitle_scorer as testee


class TestJobTitleScorer(unittest.TestCase):
    def test_normalize_returns_rank_between_0_and_1(self):
        assert_that(testee.normalize(0.6), is_(0.6))
        assert_that(testee.normalize(1.2), is_(1 / 1.2))

    def test_calc_score_calculates_correct_score(self):
        # arrange
        features = {'tag': 'h1', 'matches': [('Polymechaniker', 1)]}
        # act
        score = testee.calculate_score(features)
        # assert
        assert_that(score, is_(0.6))

    def test_calc_score_calculates_correct_score_ratio(self):
        # arrange
        features1 = {'tag': 'h2', 'matches': [('Polymechaniker', 1)]}
        features2 = {'tag': 'h1', 'matches': [('Polymechaniker', 1)]}
        # act
        score1 = testee.calculate_score(features1)
        score2 = testee.calculate_score(features2)
        # assert
        assert_that(score2, is_(greater_than(score1)))
