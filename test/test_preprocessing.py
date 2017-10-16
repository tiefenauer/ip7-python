import unittest

from bs4 import *
from bs4 import Tag
from hamcrest import *

from src import preprocessing


def read_sample_file(filename):
    with open('./resources/' + filename + '.html', 'r', encoding='utf-8') as file:
        return file.read()


def write_extracted_tags(extracted_tags, filename):
    with open('./resources/' + filename + '_extracted.html', 'w+', encoding='utf-8') as file:
        for tag in extracted_tags:
            file.write(str(tag) + '\n')


class TestPreprocessing(unittest.TestCase):
    def test_parse(self):
        # arrange
        markup = read_sample_file('sample_vacancy')
        # act
        soup = preprocessing.parse(markup)
        # assert
        assert_that(soup, equal_to(BeautifulSoup(markup, 'html.parser')))

    def test_remove_html_clutter_should_remove_clutter(self):
        # arrange
        soup_cluttered = BeautifulSoup(read_sample_file('sample_vacancy'), 'html.parser')
        # act
        extracted_tags = preprocessing.remove_html_clutter(soup_cluttered)
        # assert
        soup_expected = BeautifulSoup(read_sample_file('sample_vacancy_extracted'), 'html.parser')
        expected_tags = [child for child in soup_expected.children if type(child) is Tag]
        assert_that(extracted_tags, equal_to(expected_tags))

    def test_remove_stopwords_should_remove_stopwords(self):
        result = preprocessing.remove_stop_words("Man ist nur dann ein Superheld, wenn man sich selbst für super hält!")
        assert_that(result, is_('Man Superheld, super hält!'))
