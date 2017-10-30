import collections
import unittest

import bs4
from hamcrest import *

from src.classifier.jobtitle_feature_based import FeatureBasedJobTitleClassification, extract_job_titles, \
    extract_features

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
        features = extract_features(tag)
        # assert
        assert_that(features['tag'], is_('p'))
        assert_that(features['matches'], instance_of(collections.Iterable))
        assert_that(features['matches'], is_(empty()))

    def test_extract_features_one_match_returns_correct_match(self):
        # arrange
        tag = create_tag('h2', 'Wir suchen einen Polymechaniker (m/w) der gerne arbeitet')
        # act
        features = extract_features(tag)
        # assert
        assert_that(features['tag'], is_('h2'))
        assert_that(features['matches'], instance_of(collections.Iterable))
        assert_that(features['matches'], contains_inanyorder(('Polymechaniker', 1)))

    def test_extract_features_multiple_match_matches_are_sorted_descending(self):
        # arrange
        tag = create_tag('h2', 'Koch Polymechaniker Polymechaniker Polymechaniker Priester Priester')
        # act
        features = extract_features(tag)
        # assert
        assert_that(features['tag'], is_('h2'))
        assert_that(features['matches'], instance_of(collections.Iterable))
        assert_that(features['matches'], contains(
            ('Polymechaniker', 3),
            ('Priester', 2),
            ('Koch', 1)
        ))

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

    def test_calc_score_missing_key_calculates_default_score(self):
        # arrange
        features = {'tag': 'p', 'matches': [('Polymechaniker', 1)]}
        # act
        score = testee.calculate_score(features)
        # assert
        assert_that(score, is_(0.1))

    def test_normalize_returns_rank_between_0_and_1(self):
        assert_that(testee.normalize(0.6), is_(0.6))
        assert_that(testee.normalize(1.2), is_(1 / 1.2))

    def test_extract_job_title_returns_correct_job(self):
        # arrange
        tag = '<h2>Polymechaniker</h2>'
        # act
        result = extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_with_variant_slash_hyphen_in_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Polymechaniker/-in</h2>'
        # act
        result = extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_with_variant_slash_hyphen_euse_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Coiffeur/-euse</h2>'
        # act
        result = extract_job_titles(tag, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Coiffeur', 1)
        ))

    def test_extract_job_title_with_variant_slash_hyphen_frau_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Kaufmann/-frau</h2>'
        # act
        result = extract_job_titles(tag, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Kaufmann', 1)
        ))

    def test_extract_job_title_with_variant_slash_in_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Polymechaniker/in</h2>'
        # act
        result = extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_with_variant_slash_euse_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Coiffeur/euse</h2>'
        # act
        result = extract_job_titles(tag, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Coiffeur', 1)
        ))

    def test_extract_job_title_with_variant_slash_frau_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Kaufmann/frau</h2>'
        # act
        result = extract_job_titles(tag, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Kaufmann', 1)
        ))

    def test_extract_job_title_with_variant_mw_returns_correct_job_title(self):
        # arrange
        tag = '<h2>Polymechaniker (m/w)</h2>'
        # act
        result = extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1)
        ))

    def test_extract_job_title_multi_returns_correct_job_count(self):
        # arrange
        tag = '<h2>Polymechaniker oder Polymechanikerin</h2>'
        # act
        result = extract_job_titles(tag, ['Polymechaniker'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 2)
        ))

    def test_extract_job_title_multi_variants_returns_correct_job_count(self):
        # arrange
        tag = '<h2>Coiffeur/-euse, Polymechaniker/in, Kaufmann (m/w)</h2>'
        # act
        result = extract_job_titles(tag, ['Polymechaniker', 'Coiffeur', 'Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder(
            ('Polymechaniker', 1),
            ('Coiffeur', 1),
            ('Kaufmann', 1)
        ))
