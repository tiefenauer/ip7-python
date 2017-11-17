import unittest

from hamcrest import assert_that, is_
from pony.orm import db_session

from src.database.DataSource import DataSource
from src.database.entities_x28 import Data_Train

with db_session:
    train_data_count = Data_Train.select().count()


class DummyArgs(object):
    def __init__(self):
        self.limit = None
        self.offset = None


def create_args(limit=1.0, offset=0.0):
    args = DummyArgs()
    args.limit = limit
    args.offset = offset
    return args


def count_items(testee):
    return sum(1 for item in testee)


class TestDataSource(unittest.TestCase):
    def test_limit_offset_no_limit_no_offset_returns_all_rows(self):
        # arrange
        args = create_args()
        # act
        testee = DataSource(args, Data_Train)
        # assert
        assert_that(count_items(testee), is_(train_data_count))
        assert_that(testee.offset, is_(0))
        assert_that(testee.limit, is_(train_data_count))
        assert_that(testee.num_total, is_(train_data_count))
        assert_that(testee.num_rows, is_(train_data_count))

    def test_limit_offset_no_limit_with_offset_returns_all_rows_from_offset(self):
        # arrange
        offset = 0.1
        # act
        testee = DataSource(create_args(offset=offset), Data_Train)
        # assert
        assert_that(count_items(testee), is_(train_data_count))
        assert_that(testee.offset, is_(int(train_data_count * offset)))
        assert_that(testee.limit, is_(train_data_count))
        assert_that(testee.num_total, is_(train_data_count))
        assert_that(testee.num_rows, is_(testee.num_total - testee.offset))

    def test_limit_offset_with_limit_no_offset_returns_all_rows_to_limit(self):
        # arrange
        limit = 0.5
        # act
        testee = DataSource(create_args(limit=limit), Data_Train)
        # assert
        assert_that(count_items(testee), is_(train_data_count))
        assert_that(testee.offset, is_(0))
        assert_that(testee.limit, is_(int(train_data_count * limit)))
        assert_that(testee.num_total, is_(train_data_count))
        assert_that(testee.num_rows, is_(int(train_data_count * limit)))

    def test_limit_offset_with_limit_with_offset_returns_all_rows_from_offset_to_limit(self):
        # arrange
        offset = 0.1
        limit = 0.5
        # act
        testee = DataSource(create_args(offset=offset, limit=limit), Data_Train)
        # assert
        assert_that(count_items(testee), is_(train_data_count))
        assert_that(testee.offset, is_(int(train_data_count * offset)))
        assert_that(testee.limit, is_(int(train_data_count * limit)))
        assert_that(testee.num_total, is_(train_data_count))
        assert_that(testee.num_rows, is_(testee.limit - testee.offset))
