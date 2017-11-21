import collections
import datetime
import unittest

from hamcrest import *

import src.util.semantic_util
from src.util import util as testee

lorem_ipsum = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut ' \
              'labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores ' \
              'et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ' \
              'ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et ' \
              'dolore magna aliquyam erat, sed diam voluptua. '


class TestUtil(unittest.TestCase):
    def test_find_str1_in_str2_should_return_correct_indices(self):
        # arrange/act
        result = testee.find_str1_in_str2('sed', lorem_ipsum)
        # assert
        assert_that(result, contains_inanyorder(57, 137, 353, 433))

    def test_find_str1_in_str2_should_work_with_unescaped_characters(self):
        # arrange
        str1_with_unescaped_chars = 'C++ Programmierer'
        str2 = 'blablablabla C++ Programmierer blabblablabl'
        # act
        result = testee.find_str1_in_str2(str1_with_unescaped_chars, str2)
        # assert
        assert_that(len(list(result)), is_(1))

    def test_create_contexts_should_produce_correct_contexts(self):
        # arrange/act
        result = testee.create_contexts(lorem_ipsum, 'sed')
        # assert
        assert_that(result, contains_inanyorder(
            '...ng elitr, sed diam nonu...',
            '...yam erat, sed diam volu...',
            '...ng elitr, sed diam nonu...',
            '...yam erat, sed diam volu...'
        ))

    def test_create_contexts_should_trim_whitespace(self):
        # arrange
        text = "bli create_result_item_with_contexts blu blö                   keyword                                 lorem ipsum dolor"
        # act
        result = testee.create_contexts(text, 'keyword')
        # assert
        assert_that(result, contains_inanyorder('...s blu blö keyword lorem ips...'))

    def test_flatten_flattens_list(self):
        # arrange
        list_a = ['a', 'b', 'c', 'd']
        list_b = ['c', 'd', 'e', 'f']
        # act
        result = list(testee.flatten([list_a, list_b]))
        # assert
        assert_that(result, is_(list_a + list_b))

    def test_gen2it_returns_iterator(self):
        # arrange
        gen = (1, 2, 3, 4)
        # act
        result = testee.gen2it(gen)
        # assert
        assert_that(result, is_(instance_of(collections.Iterable)))
        for item in result:
            assert_that(item, is_(greater_than(0)))
