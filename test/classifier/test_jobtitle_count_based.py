import unittest

from hamcrest import *

from src.classifier.fts_classifier_jobtitle_count import CountBasedJobTitleClassification, find_all_matches
from src.preprocessing.preprocessor_fts import FtsPreprocessor
from test.util.test_util import create_dummy_args

args = create_dummy_args()
preprocessor = FtsPreprocessor()
testee = CountBasedJobTitleClassification(args, preprocessor)


class TestJobtitleStrategyCount(unittest.TestCase):
    def test_classify_should_return_best_match(self):
        # arrange
        dom = '<p>Schneider Schneider Schneider Koch Koch Koch Koch Sekretär</p>'
        testee.job_names = ['Schneider', 'Koch', 'Sekretär']
        # act
        (result, count, score) = testee._classify(dom)
        # assert
        assert_that(result, is_('Koch'))
        assert_that(count, is_(4))

    def test_find_all_should_return_matches(self):
        # arrange
        dom = '<p>Franz jagt im komplett verwahrlosten Taxi quer durch Bayern</p>'
        testee.job_names = ['Taxi', 'Bayern']
        # act
        result = testee.find_all(dom)
        # assert
        assert_that(result, contains_inanyorder(
            (1, 'Taxi'),
            (1, 'Bayern')
        ))

    def test_find_all_multiple_should_return_all_matches(self):
        # arrange
        dom = '<p>Taxi Taxi Bayern Bayern Bayern</p>'
        testee.job_names = ['Taxi', 'Bayern']
        # act
        result = testee.find_all(dom)
        # assert
        assert_that(result, contains_inanyorder(
            (2, 'Taxi'),
            (3, 'Bayern')
        ))

    def test_find_all_should_not_return_empty_matches(self):
        # arrance
        dom = '<p>Franz jagt im komplett verwahrlosten Taxi quer durch Bayern</p>'
        testee.job_names = ['Arzt']
        # act
        result = testee.find_all(dom)
        #
        assert_that(list(result), is_(empty()))

    def test_find_all_returns_all_matches_with_count(self):
        # arrange
        tags = [
            '<p>Assistent</p>',
            '<p>Koch Koch</p>',
            '<p>Schneider Schneider Schneider</p>'
        ]
        # act
        result = find_all_matches(tags, ['Koch', 'Schneider', 'Assistent'])
        # assert
        assert_that(result, contains_inanyorder(
            (1, 'Assistent'),
            (2, 'Koch'),
            (3, 'Schneider')
        ))

    def test_find_all_returns_variants_as_one_suffix_er(self):
        # arrange
        tags = ['<p>Schneider Schneiderin Schneider/-in Schneider/in Schneider (m/w)</p>']
        # act
        result = find_all_matches(tags, ['Schneider'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Schneider')))

    def test_find_all_returns_variants_as_one_suffix_eur(self):
        # arrange
        tags = ['<p>Coiffeur Coiffeuse Coiffeur/-euse Coiffeur/euse Coiffeur (m/w)</p>']
        # act
        result = find_all_matches(tags, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Coiffeur')))

    def test_find_all_returns_variants_as_one_suffix_mann(self):
        # arrange
        tags = ['<p>Kaufmann Kauffrau Kaufmann/-frau Kaufmann/frau Kaufmann (m/w)</p>']
        # act
        result = find_all_matches(tags, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Kaufmann')))
