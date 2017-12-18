import unittest

from hamcrest import assert_that, is_, only_contains

from src.util import loe_util


class LoeUtilTest(unittest.TestCase):

    def test_is_single_percentage_returns_correct_value(self):
        # positive tests
        assert_that(loe_util.is_single_percentage('100%'), is_(True))
        assert_that(loe_util.is_single_percentage('80%'), is_(True))
        assert_that(loe_util.is_single_percentage('67%'), is_(True))
        # negative tests
        assert_that(loe_util.is_single_percentage(''), is_(False))
        assert_that(loe_util.is_single_percentage('60-80%'), is_(False))
        assert_that(loe_util.is_single_percentage('60 -80%'), is_(False))
        assert_that(loe_util.is_single_percentage('60- 80%'), is_(False))
        assert_that(loe_util.is_single_percentage('60-80 %'), is_(False))
        assert_that(loe_util.is_single_percentage('60 - 80%'), is_(False))
        assert_that(loe_util.is_single_percentage('60- 80 %'), is_(False))
        assert_that(loe_util.is_single_percentage('80 -100 %'), is_(False))
        assert_that(loe_util.is_single_percentage('80 - 100 %'), is_(False))

    def test_is_percent_range_returns_correct_value(self):
        # positive tests
        assert_that(loe_util.is_percentate_range('60-80%'), is_(True))
        assert_that(loe_util.is_percentate_range('60 -80%'), is_(True))
        assert_that(loe_util.is_percentate_range('60- 80%'), is_(True))
        assert_that(loe_util.is_percentate_range('60-80 %'), is_(True))
        assert_that(loe_util.is_percentate_range('60 - 80%'), is_(True))
        assert_that(loe_util.is_percentate_range('60- 80 %'), is_(True))
        assert_that(loe_util.is_percentate_range('80 -100 %'), is_(True))
        assert_that(loe_util.is_percentate_range('80 - 100 %'), is_(True))

        # negative tests
        assert_that(loe_util.is_percentate_range(''), is_(False))
        assert_that(loe_util.is_percentate_range('100%'), is_(False))
        assert_that(loe_util.is_percentate_range('80%'), is_(False))
        assert_that(loe_util.is_percentate_range('67%'), is_(False))

    def test_find_all_loe_finds_all_loe(self):
        assert_that(list(loe_util.find_all_loe('80%')), only_contains('80%'))
        assert_that(list(loe_util.find_all_loe('100%')), only_contains('100%'))
        assert_that(list(loe_util.find_all_loe('80-100%')), only_contains('80-100%'))

    def test_remove_percentage_removes_single_percentages(self):
        assert_that(loe_util.remove_percentage('Schreiner 80%'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 100%'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 80-100%'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 60-80%'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 80%-100%'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 60%-80%'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 80 - 100 %'), is_('Schreiner'))
        assert_that(loe_util.remove_percentage('Schreiner 60 - 80 %'), is_('Schreiner'))
