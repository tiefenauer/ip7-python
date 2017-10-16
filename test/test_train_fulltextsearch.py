import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

import src.train.util
from src import train_fulltextsearch as testee

lorem_ipsum = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut ' \
              'labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores ' \
              'et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ' \
              'ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et ' \
              'dolore magna aliquyam erat, sed diam voluptua. '


class IsResultMatchingJob(BaseMatcher):
    def __init__(self, job_name):
        self.job_name = job_name

    def _matches(self, item):
        return item['job_name'] == self.job_name

    def describe_to(self, description):
        description.append_text('result item with item.job_name matching \'') \
            .append_text(self.job_name) \
            .append_text('\'')


def result_item_with_job(job_name):
    return IsResultMatchingJob(job_name)


class TestFullTextSearch(unittest.TestCase):
    def test_match_with_whitelist(self):
        # arrange
        row = {
            'id': 123,
            'dom': 'Lorem Arzt ipsum dolor sit amet, Bauer consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
        }
        job_names = ['Arzt', 'Lehrer', 'Bauer']
        # act
        result = testee.match_with_whitelist(row, job_names)
        # assert
        assert_that(list(result), contains_inanyorder(
            result_item_with_job('Arzt'),
            result_item_with_job('Bauer'),
        ))

    def test_find_string_occurences(self):
        # arrange/act
        result = src.train.util.find_str1_in_str2('sed', lorem_ipsum)
        # assert
        assert_that(result, contains_inanyorder(57, 137, 353, 433))

    def test_find_string_occurences_with_escape_characters(self):
        # arrange
        str1_with_unescaped_chars = 'C++ Programmierer'
        str2 = 'blablablabla C++ Programmierer blabblablabl'
        result = src.train.util.find_str1_in_str2(str1_with_unescaped_chars, str2)
        assert_that(len(result), is_(1))

    def test_create_contexts(self):
        # arrange/act
        result = src.train.util.create_contexts(lorem_ipsum, 'sed')
        # assert
        assert_that(result, contains_inanyorder(
            '...ng elitr, sed diam nonu...',
            '...yam erat, sed diam volu...',
            '...ng elitr, sed diam nonu...',
            '...yam erat, sed diam volu...'
        ))

    def test_create_contexts_with_whitespaces(self):
        # arrange
        text = "bli bla blu blö                   keyword                                 lorem ipsum dolor"
        # act
        result = src.train.util.create_contexts(text, 'keyword')
        # assert
        assert_that(result, contains_inanyorder('...a blu blö keyword lorem ips...'))
