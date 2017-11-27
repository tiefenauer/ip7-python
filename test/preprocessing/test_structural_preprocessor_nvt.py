import unittest

from hamcrest import assert_that, contains

from src.preprocessing import structural_preprocessor_nvt
from src.preprocessing.structural_preprocessor_nvt import StructuralPreprocessorNVT
from test.preprocessing.test_structural_preprocessor_nv import create_dummy_row

testee = StructuralPreprocessorNVT()


class TestStructuralPreprocessorNVT(unittest.TestCase):
    def test_preprocess_single(self):
        # arrange
        markup = """
                <h1>Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.</h1>
                <p>Dies ist noch ein Inhalt.</p>
                """
        row = create_dummy_row(html=markup)
        # act
        result = testee.preprocess_single(row)
        # assert
        assert_that(result, contains(
            ('dies', 'PDS', 'h1'),
            ('ist', 'VAFIN', 'h1'),
            ('ein', 'ART', 'h1'),
            ('test', 'NN', 'h1'),
            ('zum', 'APPRART', 'h1'),
            ('schau', 'ADJA', 'h1'),
            ('ob', 'KOUS', 'h1'),
            ('es', 'PPER', 'h1'),
            ('funktioniert', 'VVFIN', 'h1'),
            ('dies', 'PDS', 'h1'),
            ('ist', 'VAFIN', 'h1'),
            ('ein', 'ART', 'h1'),
            ('anderer', 'ADJA', 'h1'),
            ('satz', 'NN', 'h1'),
            ('dies', 'PDS', 'p'),
            ('ist', 'VAFIN', 'p'),
            ('noch', 'ADV', 'p'),
            ('ein', 'ART', 'p'),
            ('inhalt', 'NN', 'p')
        ))

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

    def test_content_sents_to_wordlist_returns_wordlist(self):
        # arrange
        content_sents = [
            ('h1', 'Dies ist ein Test zum schauen ob es funktioniert'),
            ('h1', 'Dies ist ein anderer Satz'),
            ('p', 'Dies ist noch ein Inhalt')
        ]
        # act
        result = structural_preprocessor_nvt.content_sents_to_wordlist(content_sents)
        # assert
        assert_that(result, contains(
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ))

    def test_content_sents_to_wordlist_returns_wordlist_without_punctuation(self):
        # arrange
        content_sents = [
            ('h1', 'Dies ist ein Test zum schauen, ob es funktioniert.'),
            ('h1', 'Dies ist ein anderer Satz.'),
            ('p', 'Dies ist noch ein Inhalt!')
        ]
        # act
        result = structural_preprocessor_nvt.content_sents_to_wordlist(content_sents)
        # assert
        assert_that(result, contains(
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ))

    def test_add_pos_tag_adds_pos_tag_to_list(self):
        # arrange
        content_words = [
            ('h1', ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert']),
            ('h1', ['Dies', 'ist', 'ein', 'anderer', 'Satz']),
            ('p', ['Dies', 'ist', 'noch', 'ein', 'Inhalt'])
        ]
        # act
        result = structural_preprocessor_nvt.add_pos_tag(content_words)
        result = list(result)
        # assert
        assert_that(result, contains(
            ('h1', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
                    ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')]),
            ('h1', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')]),
            ('p', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')])
        ))

    def test_content_words_to_stems_converts_words_to_stem(self):
        # arrange
        content_words = [
            ('h1', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
                    ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')]),
            ('h1', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')]),
            ('p', [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')])
        ]
        # act
        result = structural_preprocessor_nvt.content_words_to_stems(content_words)
        # assert
        assert_that(result, contains(
            ('h1', [('dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('test', 'NN'), ('zum', 'APPRART'),
                    ('schau', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')]),
            ('h1', [('dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('satz', 'NN')]),
            ('p', [('dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('inhalt', 'NN')])
        ))
