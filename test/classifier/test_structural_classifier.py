import unittest

from hamcrest import assert_that, contains

from src.classifier.structural_classifier import StructuralClassifier, top_n
from src.preprocessing.preprocessor_structural import StructuralPreprocessor
from systemtest.test_TestData import create_args
from test.preprocessing.test_preprocessor_structural import create_dummy_row

args = create_args()
preprocessor = StructuralPreprocessor()
testee = StructuralClassifier(args, preprocessor)


class TestStructuralClassifier(unittest.TestCase):
    def test_top_n_returns_top_n(self):
        # arrange
        row = create_dummy_row('Baum Baum Baum Baum Baum Haus Haus Haus Haus Maler Maler Maler Bäcker Bäcker')
        tagged_words = preprocessor.preprocess_single(row)
        # act
        result = top_n(tagged_words, 'N', 3)
        # assert
        assert_that(result, contains(
            ('baum', 5),
            ('haus', 4),
            ('mal', 3)
        ))
