import unittest

from hamcrest import assert_that, is_
from pony.orm import db_session

from src.database.TestData import TestData
from src.database.entities_pg import X28_HTML
from test.util import test_util

with db_session:
    train_data_count = X28_HTML.select().count()


def count_items(testee):
    return sum(1 for item in testee)


class TestTestData(unittest.TestCase):
    def test_no_split_returns_no_rows(self):
        # arrange
        args = test_util.create_dummy_args()
        # act
        testee = TestData(args, X28_HTML)
        # assert
        assert_that(count_items(testee), is_(0))
        assert_that(testee.split, is_(train_data_count))
        assert_that(testee.num_total, is_(train_data_count))
        assert_that(testee.num_rows, is_(0))

    def test_with_split_returns_fraction_of_rows(self):
        # arrange
        split = 0.1
        # act
        testee = TestData(test_util.create_dummy_args(split=split), X28_HTML)
        # assert
        assert_that(count_items(testee), is_(train_data_count - int(train_data_count * split)))
        assert_that(testee.split, is_(int(train_data_count * split)))
        assert_that(testee.num_total, is_(train_data_count))
        assert_that(testee.num_rows, is_(testee.num_total - testee.split))
