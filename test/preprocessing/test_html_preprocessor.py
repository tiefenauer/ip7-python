import unittest

from bs4 import BeautifulSoup
from hamcrest import assert_that, is_, not_, has_item

from src.preprocessing.html_preprocessor import HTMLPreprocessor, NON_HUMAN_READABLE_TAGS
from test import testutils

testee = HTMLPreprocessor(include_title=False)


class TestHTMLPreprocessor(unittest.TestCase):

    def test_preprocess_single_extracts_all_tags(self):
        # arrange
        markup = testutils.read_sample_file('sample_vacancy')
        row = testutils.create_dummy_row(html=markup)
        # act
        extracted_tags = testee.preprocess_single(row)
        # testutils.write_markup(extracted_tags, 'sample_vacancy_all_tags')
        # assert
        soup_expected = BeautifulSoup(testutils.read_sample_file('sample_vacancy_all_tags'), 'html.parser')
        expected_tags = soup_expected.findAll()
        assert_that(len(list(extracted_tags)), is_(len(expected_tags)))

    def test_preprocess_singel_extracts_only_human_readable_tags(self):
        # arrange
        markup = testutils.read_sample_file('sample_vacancy')
        row = testutils.create_dummy_row(html=markup)
        # act
        extracted_tags = testee.preprocess_single(row)
        extracted_tags = list(extracted_tags)
        # assert
        for tag in extracted_tags:
            assert_that(NON_HUMAN_READABLE_TAGS, not_(has_item(tag.name)))
