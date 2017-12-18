import unittest

from hamcrest import assert_that, only_contains

from src.preprocessing.preproc import create_tag
from src.preprocessing.sentence_preprocessor import SentencePreprocessor
from test import testutils

testee = SentencePreprocessor()


class SentencePreprocessorTest(unittest.TestCase):

    def test_to_sentences_map_one_sentence_returns_map_tag_name_sentences(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer.'),
            create_tag('h2', 'Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        markup = '\n'.join(str(tag) for tag in html_tags)
        row = testutils.create_dummy_row(html=markup)
        # act
        result = testee.preprocess_single(row)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', 'Wir suchen einen Geschäftsführer.'),
            ('h2', 'Willst du dich bewerben?'),
            ('p', 'Erfahrung wird überbewertet!')
        ))

    def test_to_sentences_map_multi_sentence_returns_one_entry_per_sentence(self):
        # arrange
        html_tags = [
            create_tag('h1', 'Wir suchen einen Geschäftsführer. Willst du dich bewerben?'),
            create_tag('p', 'Erfahrung wird überbewertet!')
        ]
        markup = '\n'.join(str(tag) for tag in html_tags)
        row = testutils.create_dummy_row(html=markup)
        # act
        result = testee.preprocess_single(row)
        result = list(result)
        # asser
        assert_that(result, only_contains(
            ('h1', 'Wir suchen einen Geschäftsführer.'),
            ('h1', 'Willst du dich bewerben?'),
            ('p', 'Erfahrung wird überbewertet!')
        ))
