import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

import src.classifier.classifier_jobtitle as testee


def create_row(dom_str, id=1):
    return {
        'id': id,
        'dom': dom_str
    }


class TestJobTitleClassifier(unittest.TestCase):
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
