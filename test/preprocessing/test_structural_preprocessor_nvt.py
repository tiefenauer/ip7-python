import unittest

from hamcrest import assert_that, contains

from src.preprocessing import structural_preprocessor_nvt


class TestStructuralPreprocessorNVT(unittest.TestCase):
    def test_split_tag_content_splits_into_tag_and_content(self):
        # arrange
        markup = """
        <h1>Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.</h1>
        <p>Dies ist noch ein Inhalt.</p>
        """
        # act
        html_tags, contents = structural_preprocessor_nvt.split_tag_content(markup)
        # assert
        assert_that(html_tags, contains('h1', 'p'))
        assert_that(contents, contains(
            'Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.',
            'Dies ist noch ein Inhalt.'
        ))

    def test_contents_to_sentences(self):
        # arrange
        contents = [
            'Dies ist ein Test zum schauen ob es funktioniert. Dies ist ein anderer Satz.',
            'Dies ist noch ein Inhalt.'
        ]
        html_tags = ['h1', 'p']
        # act
        result = structural_preprocessor_nvt.contents_to_sentences(contents, html_tags)
        # assert
        assert_that(result, contains(
            ('h1', 'Dies ist ein Test zum schauen ob es funktioniert.'),
            ('h1', 'Dies ist ein anderer Satz.'),
            ('p', 'Dies ist noch ein Inhalt.')
        ))

    def test_extract_words_list_returns_words_lists(self):
        # arrange
        sentences = [
            ['Dies ist ein Test zum schauen ob es funktioniert', 'Dies ist ein anderer Satz'],
            ['Dies ist noch ein Inhalt']
        ]
        # act
        result = structural_preprocessor_nvt.extract_words_list(sentences)
        # assert
        assert_that(result, contains(
            [
                ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
                ['Dies', 'ist', 'ein', 'anderer', 'Satz']
            ],
            [
                ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
            ]
        ))

    def test_extract_words_list_returns_words_lists_without_punctuation(self):
        # arrange
        sentences = [
            ['Dies ist ein Test zum schauen, ob es funktioniert.', 'Dies ist ein anderer Satz.'],
            ['Dies ist noch ein Inhalt.']
        ]
        # act
        result = structural_preprocessor_nvt.extract_words_list(sentences)
        # assert
        assert_that(result, contains(
            [
                ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
                ['Dies', 'ist', 'ein', 'anderer', 'Satz']
            ],
            [
                ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
            ]
        ))

    def test_extract_pos_tag_extracts_pos_tags(self):
        # arrange
        words_lists = [
            ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
            ['Dies', 'ist', 'ein', 'anderer', 'Satz']
        ]
        # act
        result = structural_preprocessor_nvt.extract_pos_tags(words_lists)
        # assert
        assert_that(result, contains(
            ['PDS', 'VAFIN', 'ART', 'NN', 'APPRART', 'ADJA', 'KOUS', 'PPER', 'VVFIN'],
            ['PDS', 'VAFIN', 'ART', 'ADJA', 'NN']
        ))
