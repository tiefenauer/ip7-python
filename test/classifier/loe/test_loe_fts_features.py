import unittest

from hamcrest import assert_that, is_

from src.classifier.loe import loe_fts_features


class TestLoeFtsFeatures(unittest.TestCase):

    def test_calculate_tag_weight_calculates_tag_weight(self):
        # arrange
        tag_weight_other = len(loe_fts_features.tag_ordering) + 1
        # act/assert
        assert_that(loe_fts_features.calculate_tag_weight('h1'), is_(0))
        assert_that(loe_fts_features.calculate_tag_weight('h2'), is_(0))
        assert_that(loe_fts_features.calculate_tag_weight('h3'), is_(0))
        assert_that(loe_fts_features.calculate_tag_weight('h4'), is_(0))
        assert_that(loe_fts_features.calculate_tag_weight('h4'), is_(0))
        assert_that(loe_fts_features.calculate_tag_weight('strong'), is_(1))
        assert_that(loe_fts_features.calculate_tag_weight('p'), is_(2))
        assert_that(loe_fts_features.calculate_tag_weight('span'), is_(tag_weight_other))
        assert_that(loe_fts_features.calculate_tag_weight('li'), is_(tag_weight_other))
