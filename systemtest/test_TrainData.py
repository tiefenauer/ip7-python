import math
import unittest

from hamcrest import assert_that, is_, greater_than
from pony.orm import db_session

from src.database.TrainData import TrainData
from src.database.entities_pg import X28_HTML
from test import testutils

with db_session:
    train_data_count = X28_HTML.select().count()


def count_items(testee):
    return sum(1 for item in testee)


class TestTrainData(unittest.TestCase):
    def test_no_split_returns_all_rows(self):
        # arrange
        args = testutils.create_dummy_args()
        # act
        testee = TrainData(args, X28_HTML)
        # assert
        assert_that(count_items(testee), is_(train_data_count))
        assert_that(len(testee), is_(train_data_count))
        assert_that(testee.row_from(), is_(None))
        assert_that(testee.row_to(), is_(greater_than(0)))

    def test_with_split_returns_fraction_of_rows(self):
        # arrange
        split = 0.1
        args = testutils.create_dummy_args(split=split)
        expected_count = math.floor(train_data_count * split)
        # act
        testee = TrainData(args, X28_HTML)
        # assert
        assert_that(count_items(testee), is_(expected_count))
        assert_that(len(testee), is_(expected_count))
        assert_that(testee.row_from(), is_(None))
        assert_that(testee.row_to(), is_(greater_than(0)))
