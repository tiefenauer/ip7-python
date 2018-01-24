import unittest

from hamcrest import assert_that, is_
from pony.orm import db_session

import test.testutils
from src.database.test_data import TestData
from src.database.entities_pg import X28_HTML
from test import testutils

with db_session:
    train_data_count = X28_HTML.select().count()


def count_items(testee):
    return sum(1 for item in testee)


class TestTestData(unittest.TestCase):
    def test_no_split_returns_no_rows(self):
        # arrange
        args = test.testutils.create_dummy_args()
        # act
        testee = TestData(args, X28_HTML)
        # assert
        assert_that(count_items(testee), is_(0))
        assert_that(len(testee), is_(0))
        assert_that(testee.row_from(), is_(train_data_count))
        assert_that(testee.row_to(), is_(train_data_count))

    def test_with_split_returns_fraction_of_rows(self):
        # arrange
        split = 0.1
        args = testutils.create_dummy_args(split=split)
        expected_split = int(train_data_count * split)
        expected_count = train_data_count - expected_split
        # act
        testee = TestData(args, X28_HTML)
        # assert
        assert_that(count_items(testee), is_(expected_count))
        assert_that(len(testee), is_(expected_count))
        assert_that(testee._split_row, is_(expected_split))
        assert_that(testee.row_from(), is_(expected_split))
        assert_that(testee.row_to(), is_(train_data_count))
