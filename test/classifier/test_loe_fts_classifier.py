import unittest

from bs4 import BeautifulSoup
from hamcrest import assert_that, contains, is_

from src.classifier.loe import loe_fts_classifier
from src.classifier.loe.loe_fts_classifier import LoeFtsClassifier
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
testee = LoeFtsClassifier(args)


class TestLoeFtsClassifier(unittest.TestCase):

    def test_classify_without_patterns_returns_none(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung als Maurer'),
            ('h1', 'Anstellung als Baggeführer')
        ])
        # act
        result_min, result_max = testee.classify(tags)
        # assert
        assert_that(result_min, is_(100))
        assert_that(result_max, is_(100))

    def test_classify_xxxP_returns_xxx_for_min_and_max(self):
        # arrange
        tags1 = create_tags([('h1', 'Anstellung 80% als Maurer')])
        tags2 = create_tags([('h1', 'Anstellung 80 % als Maurer')])
        # act / Assert
        assert_that(testee.classify(tags1), is_((80, 80)))
        assert_that(testee.classify(tags2), is_((80, 80)))

    def test_classify_xxx_yyyP_returns_xxx_for_min_and_yyy_max(self):
        # arrange
        tags1 = create_tags([('h1', 'Anstellung 80-100% als Maurer')])
        tags2 = create_tags([('h1', 'Anstellung 80 -100% als Maurer')])
        tags3 = create_tags([('h1', 'Anstellung 80- 100% als Maurer')])
        tags4 = create_tags([('h1', 'Anstellung 80-100 % als Maurer')])
        tags5 = create_tags([('h1', 'Anstellung 80 - 100 % als Maurer')])
        tags6 = create_tags([('h1', 'Anstellung 80 - 100% als Maurer')])
        # act/assert
        assert_that(testee.classify(tags1), is_((80, 100)))
        assert_that(testee.classify(tags2), is_((80, 100)))
        assert_that(testee.classify(tags3), is_((80, 100)))
        assert_that(testee.classify(tags4), is_((80, 100)))
        assert_that(testee.classify(tags5), is_((80, 100)))
        assert_that(testee.classify(tags6), is_((80, 100)))

    def test_classify_xxxP_yyyP_returns_xxx_for_min_and_yyy_max(self):
        # arrange
        tags1 = create_tags([('h1', 'Anstellung 80%-100% als Maurer')])
        tags2 = create_tags([('h1', 'Anstellung 80 %-100% als Maurer')])
        tags3 = create_tags([('h1', 'Anstellung 80% -100% als Maurer')])
        tags4 = create_tags([('h1', 'Anstellung 80%- 100% als Maurer')])
        tags5 = create_tags([('h1', 'Anstellung 80%-100 % als Maurer')])
        tags6 = create_tags([('h1', 'Anstellung 80 % - 100 % als Maurer')])
        tags7 = create_tags([('h1', 'Anstellung 80% - 100% als Maurer')])
        tags8 = create_tags([('h1', 'Anstellung 80%-100% als Maurer')])
        # act/assert
        assert_that(testee.classify(tags1), is_((80, 100)))
        assert_that(testee.classify(tags2), is_((80, 100)))
        assert_that(testee.classify(tags3), is_((80, 100)))
        assert_that(testee.classify(tags4), is_((80, 100)))
        assert_that(testee.classify(tags5), is_((80, 100)))
        assert_that(testee.classify(tags6), is_((80, 100)))
        assert_that(testee.classify(tags7), is_((80, 100)))
        assert_that(testee.classify(tags8), is_((80, 100)))

    def test_classify_with_multiple_patterns_returns_most_frequent_pattern(self):
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
        loe_min, loe_max = testee.classify(tags)
        # assert
        assert_that(loe_min, is_(80))
        assert_that(loe_max, is_(100))

    def test_find_loe_patterns_by_tag_returns_tags_and_results(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung 80%-100% als Maurer'),
            ('h2', 'Anstellung 80% als Baggerführer'),
            ('p', 'Anstellung 80-100% als Schreiner')
        ])
        # act
        result = loe_fts_classifier.find_loe_patterns_by_tag(tags)
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
        result = loe_fts_classifier.group_loe_patterns_by_count(tags)
        # assert
        assert_that(result, contains(
            ('80%-100%', 'h1', 2),
            ('60-80%', 'h2', 2),
            ('80%-100%', 'h2', 1),
            ('80%', 'h1', 1)
        ))

    def test_group_patterns_by_count_filters_only_percentage(self):
        # arrange
        tags = create_tags([
            ('h1', 'Anstellung 80-100 als Maurer'),
            ('h1', 'Anstellung 80-100 als Maurer'),
            ('h2', 'Anstellung 80-100 als Maurer'),
            ('h1', 'Anstellung 80% als Maurer')
        ])
        # act
        result = loe_fts_classifier.group_loe_patterns_by_count(tags)
        # assert
        assert_that(result, contains(
            ('80%', 'h1', 1)
        ))
