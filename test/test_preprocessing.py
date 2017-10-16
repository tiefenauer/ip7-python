import unittest
from src import preprocessing


class TestPreprocessing(unittest.TestCase):
    def test_remove_html_clutter_should_remove_clutter(self):
        markup = """<html>
            <head><title>Sample page</title></head>
            <body>
                <p>This is some relevant text</p>
            </body>
            </html>"""
        result = preprocessing.remove_html_clutter(markup)
        self.assertEqual()
        
    def test_remove_stopwords_should_remove_stopwords(self):
        result = preprocessing.remove_stop_words("Man ist nur dann ein Superheld, wenn man sich selbst für super hält!")
        self.assertEqual(result, "Man Superheld, super hält!")
