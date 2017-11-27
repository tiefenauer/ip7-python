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

    def test_split_words_by_tag_splits_into_words(self):
        # arrange
        markup = """
        <h1>Dies ist ein Test zum schauen ob es funktioniert. Dies ist ein anderer Satz.</h1>
        <p>Dies ist noch ein Inhalt.</p>
        """
        # act
        result = structural_preprocessor_nvt.split_words_by_tag(markup)
        tags, word_lists = zip(*result)
        # assert
        assert_that(tags, contains('h1', 'h1', 'p'))
        assert_that(word_lists, contains(
            ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
            ['Dies', 'ist', 'ein', 'anderer', 'Satz'],
            ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
        ))

    def test_content_sents_to_wordlist_returns_wordlist_without_punctuation(self):
        # arrange
        markup = """
        <h1>Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.</h1>
        <p>Dies ist noch ein Inhalt.</p>
        """
        # act
        result = structural_preprocessor_nvt.split_words_by_tag(markup)
        tags, word_lists = zip(*result)
        # assert
        assert_that(tags, contains('h1', 'h1', 'p'))
        assert_that(word_lists, contains(
            ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
            ['Dies', 'ist', 'ein', 'anderer', 'Satz'],
            ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
        ))

    def test_add_pos_tag_adds_pos_tag_to_list(self):
        # arrange
        word_lists = [
            ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
            ['Dies', 'ist', 'ein', 'anderer', 'Satz'],
            ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
        ]
        # act
        result = structural_preprocessor_nvt.add_pos_tag(word_lists)
        result = list(result)
        # assert
        assert_that(result, contains(
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
             ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')]
        ))

    def test_content_words_to_stems_converts_words_to_stem(self):
        # arrange
        word_lists = [
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
             ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')]
        ]
        # act
        result = structural_preprocessor_nvt.content_words_to_stems(word_lists)
        # assert
        assert_that(result, contains(
            [('dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('test', 'NN'), ('zum', 'APPRART'),
             ('schau', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')],
            [('dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('satz', 'NN')],
            [('dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('inhalt', 'NN')]
        ))
