import unittest

from hamcrest import *

from src.classifier.jobtitle.jobtitle_fts_classifier_count_based import CountBasedJobtitleFtsClassifier, \
    count_job_names
from src.preprocessing.preproc import create_tag

testee = CountBasedJobtitleFtsClassifier()


class TestCountBasedJobtitleFtsClassifier(unittest.TestCase):
    def test_predict_class_should_return_best_match(self):
        # arrange
        relevant_tags = [
            create_tag('p', 'Schneider Schneider Schneider Koch Koch Koch Koch Sekretär')
        ]
        testee.known_jobs = ['Schneider', 'Koch', 'Sekretär']
        # act
        result = testee.predict_class(relevant_tags)
        # assert
        assert_that(result, is_('Koch'))

    def test_count_job_names_should_return_matches(self):
        # arrange
        dom = '<p>Franz jagt im komplett verwahrlosten Taxi quer durch Bayern</p>'
        # act
        result = count_job_names(dom, ['Taxi', 'Bayern'])
        # assert
        assert_that(result, contains_inanyorder(
            (1, 'Taxi'),
            (1, 'Bayern')
        ))

    def test_count_job_names_multiple_should_return_all_matches(self):
        # arrange
        dom = '<p>Taxi Taxi Bayern Bayern Bayern</p>'
        # act
        result = count_job_names(dom, ['Taxi', 'Bayern'])
        # assert
        assert_that(result, contains_inanyorder(
            (2, 'Taxi'),
            (3, 'Bayern')
        ))

    def test_count_job_names_should_not_return_empty_matches(self):
        # arrance
        dom = '<p>Franz jagt im komplett verwahrlosten Taxi quer durch Bayern</p>'
        # act
        result = count_job_names(dom, ['Arzt'])
        #
        assert_that(list(result), is_(empty()))

    def test_count_job_names_returns_all_matches_with_count(self):
        # arrange
        tags = [
            '<p>Assistent</p>',
            '<p>Koch Koch</p>',
            '<p>Schneider Schneider Schneider</p>'
        ]
        # act
        result = count_job_names(tags, ['Koch', 'Schneider', 'Assistent'])
        # assert
        assert_that(result, contains_inanyorder(
            (1, 'Assistent'),
            (2, 'Koch'),
            (3, 'Schneider')
        ))

    def test_count_job_names_returns_variants_as_one_suffix_er(self):
        # arrange
        tags = ['<p>Schneider Schneiderin Schneider/-in Schneider/in Schneider (m/w)</p>']
        # act
        result = count_job_names(tags, ['Schneider'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Schneider')))

    def test_count_job_names_returns_variants_as_one_suffix_eur(self):
        # arrange
        tags = ['<p>Coiffeur Coiffeuse Coiffeur/-euse Coiffeur/euse Coiffeur (m/w)</p>']
        # act
        result = count_job_names(tags, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Coiffeur')))

    def test_count_job_names_returns_variants_as_one_suffix_mann(self):
        # arrange
        tags = ['<p>Kaufmann Kauffrau Kaufmann/-frau Kaufmann/frau Kaufmann (m/w)</p>']
        # act
        result = count_job_names(tags, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Kaufmann')))
