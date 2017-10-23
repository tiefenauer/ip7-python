import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src import train_fulltextsearch as testee
from src.train.util import flatten
from test.extractor.test_jobtitle_matcher import match_item_for_job_name


def create_row(dom_str, id=1):
    return {
        'id': id,
        'dom': dom_str
    }


class TestFullTextSearch(unittest.TestCase):
    def test_find_all_should_return_matches(self):
        # arrange
        row = create_row('Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')
        # act
        result = testee.find_all(row, ['Taxi', 'Bayern'])
        # assert
        assert_that(result, only_contains(
            match_item_for_job_name('Taxi'),
            match_item_for_job_name('Bayern')
        ))

    def test_find_all_should_not_return_empty_matches(self):
        # arrance
        row = create_row('Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')
        # act
        result = testee.find_all(row, ['Arzt'])
        #
        assert_that(list(result), is_(empty()))

    def test_find_best_should_return_best_match(self):
        # arrange
        row = create_row('Schneider Schneider Schneider Koch Koch Koch Koch Sekretär')
        # act
        (result, count) = testee.find_best(row, ['Schneider', 'Koch', 'Sekretär'])
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
