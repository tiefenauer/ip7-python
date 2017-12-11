import unittest

from bs4 import Tag, BeautifulSoup
from hamcrest import assert_that, is_

from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor
from test import testutils

testee = RelevantTagsPreprocessor()


class TestRelevantTagsPreprocessor(unittest.TestCase):

    def test_preprocess_single_extracts_relevant_tags(self):
        # arrange
        markup = testutils.read_sample_file('sample_vacancy')
        row = testutils.create_dummy_row(html=markup)
        # act
        result = testee.preprocess_single(row)
        extracted_tags = list(result)
        # testutils.write_extracted_tags(extracted_tags, 'sample_vacancy_relevant_tags')
        # assert
        soup_expected = BeautifulSoup(testutils.read_sample_file('sample_vacancy_relevant_tags'), 'html.parser')
        expected_tags = [child for child in soup_expected.children if type(child) is Tag]
        assert_that(extracted_tags, is_(expected_tags))
