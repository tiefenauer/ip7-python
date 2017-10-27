import collections
import unittest

import bs4
from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

import src.classifier.classifier_jobtitle as testee


def create_row(dom_str, id=1):
    return {
        'id': id,
        'dom': dom_str
    }


def create_tag(tag_name, tag_content):
    tag = bs4.BeautifulSoup('', 'html.parser').new_tag(tag_name)
    tag.string = tag_content
    return tag


class TestJobTitleClassifier(unittest.TestCase):
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

    def test_find_all_should_return_matches(self):
        # arrange
        dom = '<p>Franz jagt im komplett verwahrlosten Taxi quer durch Bayern</p>'
        # act
        result = testee.find_all(dom, ['Taxi', 'Bayern'])
        # assert
        assert_that(result, contains_inanyorder(
            (1, 'Taxi'),
            (1, 'Bayern')
        ))

    def test_find_all_multiple_should_return_all_matches(self):
        # arrange
        dom = '<p>Taxi Taxi Bayern Bayern Bayern</p>'
        # act
        result = testee.find_all(dom, ['Taxi', 'Bayern'])
        # assert
        assert_that(result, contains_inanyorder(
            (2, 'Taxi'),
            (3, 'Bayern')
        ))

    def test_find_all_should_not_return_empty_matches(self):
        # arrance
        dom = '<p>Franz jagt im komplett verwahrlosten Taxi quer durch Bayern</p>'
        # act
        result = testee.find_all(dom, ['Arzt'])
        #
        assert_that(list(result), is_(empty()))

    def test_find_best_should_return_best_match(self):
        # arrange
        dom = '<p>Schneider Schneider Schneider Koch Koch Koch Koch Sekretär</p>'
        # act
        (result, count) = testee.find_best(dom, ['Schneider', 'Koch', 'Sekretär'])
        # assert
        assert_that(result, is_('Koch'))
        assert_that(count, is_(4))

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


def result_item_with_job(job_name):
    return IsResultMatchingJob(job_name)


class IsResultMatchingJob(BaseMatcher):
    def __init__(self, job_name):
        self.job_name = job_name

    def _matches(self, item):
        return item['job_name'] == self.job_name

    def describe_to(self, description):
        description.append_text('result item with item[\'job_name\'] matching \'') \
            .append_text(self.job_name) \
            .append_text('\'')
