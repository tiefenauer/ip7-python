import unittest

from hamcrest import assert_that, contains, empty, is_

from src.preprocessing import structural_preprocessor
from src.preprocessing.structural_preprocessor import StructuralPreprocessor
from src.preprocessing.preproc import create_tags
from test import testutils
from test.testutils import create_dummy_row

testee = StructuralPreprocessor()


class TestStructuralPreprocessor(unittest.TestCase):
    def test_preprocess_single(self):
        # arrange
        markup = """
                <h1>Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.</h1>
                <p>Dies ist noch ein Inhalt.</p>
                """
        row = testutils.create_dummy_row(html=markup)
        # act
        result = testee.preprocess_single(row)
        # assert
        assert_that(result, contains(
            ('dies', 'PDS', 'h1'),
            ('sein', 'VAFIN', 'h1'),
            ('ein', 'ART', 'h1'),
            ('test', 'NN', 'h1'),
            ('zum', 'APPRART', 'h1'),
            ('schauen', 'ADJA', 'h1'),
            ('ob', 'KOUS', 'h1'),
            ('es', 'PPER', 'h1'),
            ('funktionieren', 'VVFIN', 'h1'),
            ('dies', 'PDS', 'h1'),
            ('sein', 'VAFIN', 'h1'),
            ('ein', 'ART', 'h1'),
            ('anderer', 'ADJA', 'h1'),
            ('satz', 'NN', 'h1'),
            ('dies', 'PDS', 'p'),
            ('sein', 'VAFIN', 'p'),
            ('noch', 'ADV', 'p'),
            ('ein', 'ART', 'p'),
            ('inhalt', 'NN', 'p')
        ))

    def test_preprocess_single_no_relevant_tags(self):
        # arrange
        markup = "<img src='foo/bar.jpg'></img>"
        row = testutils.create_dummy_row(html=markup)
        # act
        result = testee.preprocess_single(row)
        # assert
        assert_that(result, is_(empty()))

    def test_split_words_by_tag_splits_into_words(self):
        # arrange
        relevant_tags = create_tags([
            ('h1', 'Dies ist ein Test zum schauen ob es funktioniert. Dies ist ein anderer Satz.'),
            ('p', 'Dies ist noch ein Inhalt.')
        ])
        # act
        result = structural_preprocessor.split_words_by_tag(relevant_tags)
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
        relevant_tags = create_tags([
            ('h1', 'Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.'),
            ('p', 'Dies ist noch ein Inhalt.')
        ])
        # act
        result = structural_preprocessor.split_words_by_tag(relevant_tags)
        tags, word_lists = zip(*result)
        # assert
        assert_that(tags, contains('h1', 'h1', 'p'))
        assert_that(word_lists, contains(
            ['Dies', 'ist', 'ein', 'Test', 'zum', 'schauen', 'ob', 'es', 'funktioniert'],
            ['Dies', 'ist', 'ein', 'anderer', 'Satz'],
            ['Dies', 'ist', 'noch', 'ein', 'Inhalt']
        ))

    def test_content_words_to_lemmata_converts_words_to_stem(self):
        # arrange
        word_lists = [
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('Test', 'NN'), ('zum', 'APPRART'),
             ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktioniert', 'VVFIN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('Satz', 'NN')],
            [('Dies', 'PDS'), ('ist', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('Inhalt', 'NN')]
        ]
        # act
        result = structural_preprocessor.content_words_to_lemmata(word_lists)
        # assert
        assert_that(result, contains(
            [('dies', 'PDS'), ('sein', 'VAFIN'), ('ein', 'ART'), ('test', 'NN'), ('zum', 'APPRART'),
             ('schauen', 'ADJA'), ('ob', 'KOUS'), ('es', 'PPER'), ('funktionieren', 'VVFIN')],
            [('dies', 'PDS'), ('sein', 'VAFIN'), ('ein', 'ART'), ('anderer', 'ADJA'), ('satz', 'NN')],
            [('dies', 'PDS'), ('sein', 'VAFIN'), ('noch', 'ADV'), ('ein', 'ART'), ('inhalt', 'NN')]
        ))
