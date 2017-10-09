from src.extractor import jobtitle
import unittest

# class JobTitleTest(unittest.TestCase):
#     def tag_matches_should_match_relevant_tags():
#         assert jobtitle.tag_matches('p')

def tag_matches_should_match_relevant_tags():
    assert jobtitle.is_relevant('p')