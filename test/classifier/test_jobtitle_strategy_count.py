import unittest

from hamcrest import *

from src.classifier.jobtitle_strategy_count import CountBasedJobTitleClassification

testee = CountBasedJobTitleClassification()


class TestJobtitleStrategyCount(unittest.TestCase):
    def test_classify_should_return_best_match(self):
        # arrange
        dom = '<p>Schneider Schneider Schneider Koch Koch Koch Koch Sekretär</p>'
        testee.job_names = ['Schneider', 'Koch', 'Sekretär']
        # act
        (result, count, score) = testee.classify(dom)
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
