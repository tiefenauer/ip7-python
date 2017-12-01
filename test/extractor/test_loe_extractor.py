import unittest
from unittest import skip

from bs4 import BeautifulSoup
from hamcrest import assert_that, contains, is_

from src.extractor import loe_extractor
from src.extractor.loe_extractor import LoeExtractor
from src.preprocessing.fts_preprocessor import FtsPreprocessor
from test.util.test_util import create_dummy_args

"""
Anstellung 100% als Maurer
Anstellung 80% als Maurer
Anstellung 80-100% als Maurer
Anstellung 60-80% als Maurer
Anstellung 80%-100% als Maurer
Anstellung 60%-80% als Maurer

"""


def create_tag(tag_name, tag_content):
    tag = BeautifulSoup('', 'html.parser').new_tag(tag_name)
    tag.string = tag_content
    return tag


def create_tags(param):
    return [create_tag(tag_name, tag_content) for (tag_name, tag_content) in param]


args = create_dummy_args()
preprocessor = FtsPreprocessor()
testee = LoeExtractor(args, preprocessor)


class TestLoeExtractor(unittest.TestCase):

    def test_extract_with_multiple_patterns_returns_most_frequent_pattern(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h2', 'Anstellung 80%-100% als Maurer'),
            ('h1', 'Anstellung 80% als Maurer'),
            ('h2', 'Anstellung 60-80% als Maurer'),
            ('h2', 'Anstellung 60-80% als Maurer')
        ])
        # act
        result = testee.extract(tags)
        # assert
        assert_that(result, is_('80%-100%'))

    def test_extract_without_patterns_returns_none(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung als Maurer'),
            ('h1', 'Anstellung als Baggeführer')
        ])
        # act
        result = testee.extract(tags)
        # assert
        assert_that(result, is_(None))

    def test_find_loe_patterns_3digits_returns_loe_patterns(self):
        # arrange
        text = 'Anstellung 100% als Maurer'
        # act
        result = loe_extractor.find_loe_patterns(text)
        # assert
        assert_that(result, contains('100%'))

    def test_find_loe_patterns_2digits_returns_loe_patterns(self):
        # arrange
        text = 'Anstellung 60% als Maurer'
        # act
        result = loe_extractor.find_loe_patterns(text)
        # assert
        assert_that(result, contains('60%'))

    def test_find_loe_patterns_2digits_2_digitsPercent_returns_loe_patterns(self):
        # arrange
        text = 'Anstellung 60-80% als Maurer'
        # act
        result = loe_extractor.find_loe_patterns(text)
        # assert
        assert_that(result, contains('60-80%'))

    def test_find_loe_patterns_2digits_3_digitsPercent_returns_loe_patterns(self):
        # arrange
        text = 'Anstellung 80-100% als Maurer'
        # act
        result = loe_extractor.find_loe_patterns(text)
        # assert
        assert_that(result, contains('80-100%'))

    def test_find_loe_patterns_2digitsPercent_2_digitsPercent_returns_loe_patterns(self):
        # arrange
        text = 'Anstellung 60%-80% als Maurer'
        # act
        result = loe_extractor.find_loe_patterns(text)
        # assert
        assert_that(result, contains('60%-80%'))

    def test_find_loe_patterns_2digitsPercent_3_digitsPercent_returns_loe_patterns(self):
        # arrange
        text = 'Anstellung 80%-100% als Maurer'
        # act
        result = loe_extractor.find_loe_patterns(text)
        # assert
        assert_that(result, contains('80%-100%'))

    def test_find_loe_patterns_by_tag_returns_tags_and_results(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h2', 'Anstellung 80% als Baggerführer'),
            ('p', 'Anstellung 80-100% als Schreiner')
        ])
        # act
        result = loe_extractor.find_loe_patterns_by_tag(tags)
        # assert
        assert_that(result, contains(
            ('80%-100%', 'h1'),
            ('80%', 'h2'),
            ('80-100%', 'p')
        ))

    def test_group_patterns_by_count_returns_list_sorted_by_count_desc(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h2', 'Anstellung 80%-100% als Maurer'),
            ('h1', 'Anstellung 80% als Maurer'),
            ('h2', 'Anstellung 60-80% als Maurer'),
            ('h2', 'Anstellung 60-80% als Maurer')
        ])
        # act
        result = loe_extractor.group_loe_patterns_by_count(tags)
        # assert
        assert_that(result, contains(
            ('80%-100%', 3),
            ('60-80%', 2),
            ('80%', 1)
        ))

    @skip("find a way to sort list by html tag and occurrence while preserving grouping")
    def test_group_loe_patterns_by_tag_returns_list_sorted_by_tag_and_count(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h2', 'Anstellung 80%-100% als Maurer'),
            ('h1', 'Anstellung 80% als Maurer'),
            ('h2', 'Anstellung 60-80% als Maurer'),
            ('h2', 'Anstellung 60-80% als Maurer')
        ])
        # random.shuffle(tags) # shuffle to check if sorting works
        # act
        result = loe_extractor.group_loe_patterns_by_tag(tags)
        # assert
        assert_that(result, contains(
            ('80%-100%', 'h1', 2),
            ('80%-100%', 'h2', 1),
            ('80%', 'h1', 1),
            ('60-80%', 'h2', 2)
        ))
