import unittest

from hamcrest import *
from hamcrest.core.base_matcher import BaseMatcher

from src.jobtitle import jobtitle_extractor as testee


class TestJobTitleExtractor(unittest.TestCase):
    def test_find_all_returns_all_matches_with_count(self):
        # arrange
        tags = [
            '<p>Assistent</p>',
            '<p>Koch Koch</p>',
            '<p>Schneider Schneider Schneider</p>'
        ]
        # act
        result = testee.find_all_matches(tags, ['Koch', 'Schneider', 'Assistent'])
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
        result = testee.find_all_matches(tags, ['Schneider'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Schneider')))

    def test_find_all_returns_variants_as_one_suffix_eur(self):
        # arrange
        tags = ['<p>Coiffeur Coiffeuse Coiffeur/-euse Coiffeur/euse Coiffeur (m/w)</p>']
        # act
        result = testee.find_all_matches(tags, ['Coiffeur'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Coiffeur')))

    def test_find_all_returns_variants_as_one_suffix_mann(self):
        # arrange
        tags = ['<p>Kaufmann Kauffrau Kaufmann/-frau Kaufmann/frau Kaufmann (m/w)</p>']
        # act
        result = testee.find_all_matches(tags, ['Kaufmann'])
        # assert
        assert_that(result, contains_inanyorder((5, 'Kaufmann')))


def result_item_with_name_and_context(job_name, context):
    return IsResultMatchingJob(job_name, context)


class IsResultMatchingJob(BaseMatcher):
    def __init__(self, job_name, job_contexts):
        self.job_name = job_name
        self.job_contexts = job_contexts

    def _matches(self, item):
        if item['job_name'] != self.job_name:
            return False
        if set(item['job_contexts']) != set(self.job_contexts):
            return False
        return True

    def describe_to(self, description):
        description.append_text('result item with item[\'job_name\'] matching \'') \
            .append_text(self.job_name) \
            .append_text('\' and item[\'job_context\'] matching \'') \
            .append_text(self.job_contexts) \
            .append_text('\'')
