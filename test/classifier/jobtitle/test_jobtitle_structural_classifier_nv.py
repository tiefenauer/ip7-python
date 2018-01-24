import os
import unittest

from hamcrest import assert_that, contains, is_, not_, only_contains

from src.classifier.jobtitle import jobtitle_classifier_structural_nv
from src.classifier.jobtitle.jobtitle_classifier_structural_nv import JobtitleStructuralClassifierNV
from src.database.X28TrainData import X28TrainData
from src.preprocessing.structural_preprocessor_nv import StructuralPreprocessorNV
from test.testutils import create_dummy_args, create_dummy_row

args = create_dummy_args()
preprocessor = StructuralPreprocessorNV()
testee = JobtitleStructuralClassifierNV(args)


class TestJobtitleStructuralClassifierNV(unittest.TestCase):
    def test_top_n_returns_top_n(self):
        # arrange
        row = create_dummy_row('Baum Baum Baum Baum Baum Haus Haus Haus Haus Maler Maler Maler Bäcker Bäcker')
        tagged_words = preprocessor.preprocess_single(row)
        # act
        result = jobtitle_classifier_structural_nv.top_n(tagged_words, 'N', 3)
        # assert
        assert_that(result, contains(
            ('baum', 5),
            ('haus', 4),
            ('maler', 3)
        ))

    def test_top_n_verbs_ignores_flexions(self):
        # arrange
        row = create_dummy_row("""sehen ich sehe sehen sehen sehen sah
                                helfen ich helfe helfen helfen half
                                machen ich mache du machst er machte
                                fahren fahrend 
                                """)
        tagged_words = preprocessor.preprocess_single(row)
        # act
        result = jobtitle_classifier_structural_nv.top_n(tagged_words, 'V', 3)
        # assert
        assert_that(result, only_contains(
            ('sehen', 6),
            ('helfen', 5),
            ('machen', 4)
        ))

    def test_extract_features_returns_top_5_nouns_and_verbs(self):
        # arrange
        row = create_dummy_row("""Baum Baum Baum Baum Baum Baum Baum 
                                  Haus Haus Haus Haus Haus Haus  
                                  Maler Maler Maler Maler Maler
                                  Bäcker Bäcker Bäcker Bäcker
                                  Auto Auto Auto 
                                  Fahrrad Fahrrad   
                                  sehen sehen sehen sehen sehen sehen sehen 
                                  backen backen backen backen backen backen 
                                  braten braten braten braten braten 
                                  kochen kochen kochen kochen 
                                  suchen suchen suchen 
                                  finden finden     
                                  """)
        tagged_words = preprocessor.preprocess_single(row)
        # act
        result = testee.extract_features(tagged_words)
        # assert
        assert_that(result['noun-1'], is_('baum'))
        assert_that(result['noun-2'], is_('haus'))
        assert_that(result['noun-3'], is_('maler'))
        assert_that(result['noun-4'], is_('bäcker'))
        assert_that(result['noun-5'], is_('auto'))
        assert_that(result['verb-1'], is_('sehen'))
        assert_that(result['verb-2'], is_('backen'))
        assert_that(result['verb-3'], is_('braten'))
        assert_that(result['verb-4'], is_('kochen'))
        assert_that(result['verb-5'], is_('suchen'))

    def test_save_load(self):
        # arrange
        testee.filename = 'test.pickle'
        labeled_data = X28TrainData(create_dummy_args(split=0.00001))
        processed_Data = StructuralPreprocessorNV(labeled_data)
        testee.train_classifier(processed_Data)
        # act
        path = testee.save_model()
        testee.filename = path
        model = testee.load_model()
        os.remove(path)
        # assert
        assert_that(model, is_(not_(None)))
