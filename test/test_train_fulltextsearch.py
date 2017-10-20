import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src import train_fulltextsearch as testee


def create_row(dom_str, id=1):
    return {
        'id': id,
        'dom': dom_str
    }


class TestFullTextSearch(unittest.TestCase):
    def test_process_row_should_return_matches(self):
        # arrange
        row = create_row('Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')
        testee.job_names = ['Taxi', 'Bayern']
        # act
        result = testee.process_row(row)
        # assert
        assert_that(result, only_contains(
            result_item_with_job('Taxi'),
            result_item_with_job('Bayern')
        ))

    def test_process_row_should_not_return_empty_matches(self):
        # arrance
        row = create_row('Franz jagt im komplett verwahrlosten Taxi quer durch Bayern')
        testee.job_names = ['Arzt']
        # act
        result = list(testee.process_row(row))
        #
        assert_that(result, is_(empty()))

    def test_find_matches_should_only_return_matched_job_names(self):
        # arrange
        dom = 'Lorem Arzt ipsum dolor sit amet, Bauer consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
        testee.job_names = ['Arzt', 'Lehrer', 'Bauer']
        # act
        result = list(testee.find_matches(dom))
        # assert
        assert_that(result, only_contains(
            result_item_with_job('Arzt'),
            result_item_with_job('Bauer'),
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
