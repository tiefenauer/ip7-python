import itertools
import unittest

from hamcrest import assert_that, is_, not_, less_than, contains

from src.classifier.jobtitle.jobtitle_fts_features import JobtitleFtsFeatures


class TestJobtitleFtsFeatures(unittest.TestCase):

    def test_eq_with_same_values_returns_True(self):
        # arrange
        feature1 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=10)
        feature2 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=10)
        # act/assert
        assert_that(feature1, is_(feature2))

    def test_eq_with_different_values_returns_False(self):
        # arrange
        parms = itertools.product(
            ('Koch', 'Arzt'),  # job name
            ('h1', 'h2'),  # highest tag
            (1, 2),  # first position
            (10, 11)  # num_occurrences
        )
        features = []
        for (job_name, highest_tag, first_position, num_occurrences) in parms:
            features.append(JobtitleFtsFeatures(job_name, highest_tag, first_position, num_occurrences))
        # act/assert
        for i in range(1, len(features)):
            assert_that(features[i - 1], is_(not_(features[i])))

    def test_lt_with_different_highest_tag_higher_tag_is_first(self):
        # arrange
        feature1 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=10)
        feature2 = JobtitleFtsFeatures(job_name='Bäcker', highest_tag_name='h2', first_tag_index=1, job_name_count=10)
        # act/assert
        assert_that(feature1, is_(less_than(feature2)))

    def test_lt_with_different_highest_tag_tag_weight_is_considered_and_not_tag_name(self):
        # arrange
        feature1 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=10)
        feature2 = JobtitleFtsFeatures(job_name='Bäcker', highest_tag_name='a', first_tag_index=1, job_name_count=10)
        # act/assert
        assert_that(feature1, is_(less_than(feature2)))

    def test_lt_with_different_position_lower_tag_is_first(self):
        # arrange
        feature1 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=10)
        feature2 = JobtitleFtsFeatures(job_name='Bäcker', highest_tag_name='h1', first_tag_index=2, job_name_count=10)
        # act/assert
        assert_that(feature1, is_(less_than(feature2)))

    def test_lt_with_different_occurrence_higher_occurrence_is_first(self):
        # arrange
        feature1 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=12)
        feature2 = JobtitleFtsFeatures(job_name='Bäcker', highest_tag_name='h1', first_tag_index=1, job_name_count=10)
        # act/assert
        assert_that(feature1, is_(less_than(feature2)))

    def test_lt_with_different_occurrence_and_different_position_higher_occurrence_is_first(self):
        # arrange
        feature1 = JobtitleFtsFeatures(job_name='Koch', highest_tag_name='h1', first_tag_index=1, job_name_count=12)
        feature2 = JobtitleFtsFeatures(job_name='Bäcker', highest_tag_name='h1', first_tag_index=0, job_name_count=10)
        # act/assert
        assert_that(feature1, is_(less_than(feature2)))

    def test_sorted_features_sorts_features_best_first(self):
        # arrange
        features = [
            JobtitleFtsFeatures(job_name='A', highest_tag_name='h1', job_name_count=1, first_tag_index=0),
            JobtitleFtsFeatures(job_name='B', highest_tag_name='h1', job_name_count=1, first_tag_index=1),
            JobtitleFtsFeatures(job_name='C', highest_tag_name='h1', job_name_count=0, first_tag_index=0),
            JobtitleFtsFeatures(job_name='D', highest_tag_name='h1', job_name_count=0, first_tag_index=1),
            JobtitleFtsFeatures(job_name='E', highest_tag_name='h2', job_name_count=1, first_tag_index=0),
            JobtitleFtsFeatures(job_name='F', highest_tag_name='h2', job_name_count=1, first_tag_index=1),
            JobtitleFtsFeatures(job_name='G', highest_tag_name='h2', job_name_count=0, first_tag_index=0),
            JobtitleFtsFeatures(job_name='H', highest_tag_name='h2', job_name_count=0, first_tag_index=1)
        ]
        # act
        result = sorted(features)
        # assert
        assert_that(result, contains(
            JobtitleFtsFeatures(job_name='A', highest_tag_name='h1', job_name_count=1, first_tag_index=0),
            JobtitleFtsFeatures(job_name='B', highest_tag_name='h1', job_name_count=1, first_tag_index=1),
            JobtitleFtsFeatures(job_name='C', highest_tag_name='h1', job_name_count=0, first_tag_index=0),
            JobtitleFtsFeatures(job_name='D', highest_tag_name='h1', job_name_count=0, first_tag_index=1),
            JobtitleFtsFeatures(job_name='E', highest_tag_name='h2', job_name_count=1, first_tag_index=0),
            JobtitleFtsFeatures(job_name='F', highest_tag_name='h2', job_name_count=1, first_tag_index=1),
            JobtitleFtsFeatures(job_name='G', highest_tag_name='h2', job_name_count=0, first_tag_index=0),
            JobtitleFtsFeatures(job_name='H', highest_tag_name='h2', job_name_count=0, first_tag_index=1)
        ))
