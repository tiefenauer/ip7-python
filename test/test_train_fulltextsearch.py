import unittest

from hamcrest import *

from src import train_fulltextsearch as testee


class TestFullTextSearch(unittest.TestCase):
    def test_match_with_whitelist(self):
        # arrange
        dom = 'Lorem Arzt ipsum dolor sit amet, Bauer consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
        job_names = ['Arzt', 'Lehrer', 'Bauer']
        # act
        result = testee.match_with_whitelist(dom, job_names)
        # assert
        assert_that(set(result), contains_inanyorder('Arzt', 'Bauer'))
