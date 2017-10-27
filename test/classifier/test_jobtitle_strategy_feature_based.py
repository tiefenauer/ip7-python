import collections
import unittest

import bs4
from hamcrest import *

from src.classifier.jobtitle_strategy_feature_based import FeatureBasedJobTitleClassification

testee = FeatureBasedJobTitleClassification()


def create_tag(tag_name, tag_content):
    tag = bs4.BeautifulSoup('', 'html.parser').new_tag(tag_name)
    tag.string = tag_content
    return tag


class TestFeatureBasedJobtitleClassification(unittest.TestCase):
    def test_classify_one_match_one_occurrence_returns_correct_match(self):
        # arrange
        tags = [
            create_tag('h1', 'Polymechaniker')
        ]
        # act
        clazz, occ, score = testee.classify(tags)
        # assert
        assert_that(clazz, is_('Polymechaniker'))
        assert_that(occ, is_(1))
        assert_that(score, is_(greater_than(0)))

    def test_classify_one_match_multi_occurrence_returns_correct_match(self):
        # arrange
        tags = [
            create_tag('h1', 'Polymechaniker oder Polymechanikerin')
        ]
        # act
        clazz, occ, score = testee.classify(tags)
        # assert
        assert_that(clazz, is_('Polymechaniker'))
        assert_that(occ, is_(2))
        assert_that(score, is_(greater_than(0)))

    def test_classify_multi_match_one_occurrence_returns_correct_match(self):
        # arrange
        tags = [
            create_tag('h1', 'Koch'),
            create_tag('h2', 'Polymechaniker')
        ]
        # act
        clazz, occ, score = testee.classify(tags)
        # assert
        assert_that(clazz, is_('Koch'))
        assert_that(occ, is_(1))
        assert_that(score, is_(greater_than(0)))

    def test_extract_features_no_match_returns_empty_list(self):
        # arrange
        tag = create_tag('p', 'nothing to see here...')
        # act
        features = testee.extract_features(tag)
        # assert
        assert_that(features['tag'], is_('p'))
        assert_that(features['matches'], instance_of(collections.Iterable))
        assert_that(features['matches'], is_(empty()))

    def test_extract_features_one_match_returns_correct_match(self):
        # arrange
        tag = create_tag('h2', 'Wir suchen einen Polymechaniker (m/w) der gerne arbeitet')
        # act
        features = testee.extract_features(tag)
        # assert
        assert_that(features['tag'], is_('h2'))
        assert_that(features['matches'], instance_of(collections.Iterable))
        assert_that(features['matches'], contains_inanyorder(('Polymechaniker', 1)))

    def test_extract_features_multiple_match_matches_are_sorted_descending(self):
        # arrange
        tag = create_tag('h2', 'Koch Polymechaniker Polymechaniker Polymechaniker Priester Priester')
        # act
        features = testee.extract_features(tag)
        # assert
        assert_that(features['tag'], is_('h2'))
        assert_that(features['matches'], instance_of(collections.Iterable))
        assert_that(features['matches'], contains(
            ('Polymechaniker', 3),
            ('Priester', 2),
            ('Koch', 1)
        ))
