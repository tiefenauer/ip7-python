import unittest
from unittest.test.testmock.support import is_instance

from hamcrest import assert_that, contains

from src.preprocessing.structural_preprocessor_nv import StructuralPreprocessorNV


class DummyRow(object):
    def __init__(self):
        self.html = None
        self.plaintext = None
        self.processed = []


def create_dummy_row(plaintext=None, html=None):
    row = DummyRow()
    row.html = html
    row.plaintext = plaintext
    return row


testee = StructuralPreprocessorNV()


class TestStructuralPreprocessorNV(unittest.TestCase):
    def test_preprocess_single_returns_tagged_words(self):
        # arrange
        row = create_dummy_row('Dies ist ein Test zum schauen ob es funktioniert')
        # act
        result = testee.preprocess_single(row)
        # assert
        assert_that(list(result), contains(
            ('dies', 'PDS'),
            ('ist', 'VAFIN'),
            ('ein', 'ART'),
            ('test', 'NN'),
            ('zum', 'APPRART'),
            ('schau', 'ADJA'),
            ('ob', 'KOUS'),
            ('es', 'PPER'),
            ('funktioniert', 'VVFIN')
        ))

    def test_preprocess_single_removes_punctuation(self):
        # arrange
        row = create_dummy_row('Dies ist ein Test zum schauen, ob es funktioniert.')
        # act
        result = testee.preprocess_single(row)
        # assert
        assert_that(list(result), contains(
            ('dies', 'PDS'),
            ('ist', 'VAFIN'),
            ('ein', 'ART'),
            ('test', 'NN'),
            ('zum', 'APPRART'),
            ('schau', 'ADJA'),
            ('ob', 'KOUS'),
            ('es', 'PPER'),
            ('funktioniert', 'VVFIN')
        ))

    def test_preprocess_single_returns_flat_list(self):
        # arrange
        row = create_dummy_row('Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.')
        # act
        result = testee.preprocess_single(row)
        # assert
        assert_that(list(result), contains(
            ('dies', 'PDS'),
            ('ist', 'VAFIN'),
            ('ein', 'ART'),
            ('test', 'NN'),
            ('zum', 'APPRART'),
            ('schau', 'ADJA'),
            ('ob', 'KOUS'),
            ('es', 'PPER'),
            ('funktioniert', 'VVFIN'),
            ('dies', 'PDS'),
            ('ist', 'VAFIN'),
            ('ein', 'ART'),
            ('anderer', 'ADJA'),
            ('satz', 'NN')
        ))

