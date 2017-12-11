import unittest

from hamcrest import assert_that, contains

import test.testutils
from src.preprocessing.structural_preprocessor_nv import StructuralPreprocessorNV
from test.util import test_util

testee = StructuralPreprocessorNV()


class TestStructuralPreprocessorNV(unittest.TestCase):
    def test_preprocess_single_returns_tagged_words(self):
        # arrange
        row = test.testutils.create_dummy_row('Dies ist ein Test zum schauen ob es funktioniert')
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
        row = test.testutils.create_dummy_row('Dies ist ein Test zum schauen, ob es funktioniert.')
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
        row = test.testutils.create_dummy_row(
            'Dies ist ein Test zum schauen, ob es funktioniert. Dies ist ein anderer Satz.')
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
