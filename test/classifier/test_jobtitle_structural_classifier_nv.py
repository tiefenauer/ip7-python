import unittest

import os
from hamcrest import assert_that, contains, is_, not_

from src.classifier.jobtitle import jobtitle_structural_classifier_nv
from src.classifier.jobtitle.jobtitle_structural_classifier_nv import JobtitleStructuralClassifierNV
from src.database.X28TrainData import X28TrainData
from src.preprocessing.structural_preprocessor_nv import StructuralPreprocessorNV
from test.util.test_util import create_dummy_args, create_dummy_row

args = create_dummy_args()
preprocessor = StructuralPreprocessorNV()
testee = JobtitleStructuralClassifierNV(args)


class TestJobtitleStructuralClassifierNV(unittest.TestCase):
    def test_top_n_returns_top_n(self):
        # arrange
        row = create_dummy_row('Baum Baum Baum Baum Baum Haus Haus Haus Haus Maler Maler Maler Bäcker Bäcker')
        tagged_words = preprocessor.preprocess_single(row)
        # act
        result = jobtitle_structural_classifier_nv.top_n(tagged_words, 'N', 3)
        # assert
        assert_that(result, contains(
            ('baum', 5),
            ('haus', 4),
            ('mal', 3)
        ))

    def test_top_n_ignores_variants(self):
        # arrange
        row = create_dummy_row("""sehen ich sehe sehen sehen sehen 
                                helfen ich helfe helfen helfen
                                schauen ich schaue schauen 
                                fahren fahrend 
                                """)
        tagged_words = preprocessor.preprocess_single(row)
        # act
        result = jobtitle_structural_classifier_nv.top_n(tagged_words, 'V', 3)
        # assert
        assert_that(result, contains(
            ('seh', 5),
            ('helf', 4),
            ('schau', 3)
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
        assert_that(result['noun-3'], is_('mal'))
        assert_that(result['noun-4'], is_('back'))
        assert_that(result['noun-5'], is_('auto'))
        assert_that(result['verb-1'], is_('seh'))
        assert_that(result['verb-2'], is_('back'))
        assert_that(result['verb-3'], is_('brat'))
        assert_that(result['verb-4'], is_('koch'))
        assert_that(result['verb-5'], is_('such'))

    def test_save_load(self):
        # arrange
        data_train = X28TrainData(create_dummy_args(split=0.00001))
        testee.train_model(data_train)
        # act
        testee.filename = 'test.pickle'
        path = testee.save_model()
        testee.filename = path
        model = testee.load_model()
        os.remove(path)
        # assert
        assert_that(model, is_(not_(None)))