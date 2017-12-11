import unittest

from src.classifier.jobtitle import jobtitle_fts_combined


class TestCombinedJobtitleFtsClassifier(unittest.TestCase):

    def test_expand_job_name_with_expandable_job_name_returns_expanded_job_name(self):
        # arrange
        # act
        jobtitle_fts_combined.expand_job_name(best_match)
        # assert
