import unittest

from bs4 import BeautifulSoup
from hamcrest import assert_that, is_

from src.preprocessing.tags_preprocessor import TagsPreprocessor
from test import testutils

testee = TagsPreprocessor()


class TestTagsPreprocessor(unittest.TestCase):

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
        assert_that(len(extracted_tags), is_(len(expected_tags)))
