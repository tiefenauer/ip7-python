import datetime
import unittest

from hamcrest import assert_that, is_

from src.util import semantic_util as testee


class TestSemanticUtil(unittest.TestCase):
    def test_parse_filename_parses_filename(self):
        # arrange
        date_format = '%Y-%m-%d-%H-%M-%S'
        f_datetime = datetime.datetime.strptime('2017-11-13-07-57-49', date_format)
        num_words = 837256
        num_features = 300
        num_minwords = 40
        num_context = 10

        filename = datetime.datetime.strftime(f_datetime, date_format) + \
                   '_{}words_{}features_{}minwords_{}context.gz'.format(num_words, 300, 40, 10)
        # act
        result = testee.parse_filename(filename)
        # assert
        assert_that(result['datetime'], is_(f_datetime))
        assert_that(result['num_words'], is_(num_words))
        assert_that(result['num_features'], is_(num_features))
        assert_that(result['num_minwords'], is_(num_minwords))
        assert_that(result['num_context'], is_(num_context))
