import unittest

from hamcrest import assert_that, is_, not_, empty

from src.preprocessing.preprocessor_structural import StructuralX28Preprocessor

testee = StructuralX28Preprocessor()


class TestStructuralX28Preprocessor(unittest.TestCase):
    def test_preprocess_single_produces_correct_tokens(self):
        # arrange
        markup = """
        <html>
            <title></title>
            <body>
                <h1>                Das ist ein Titel                   </h1>
                <p>Wir suchen einen kräftigen Bauarbeiter oder Kranführer der gerne arbeitet.
                Hier noch ein zweiter Satz zum schauen ob's funktioniert.</p>
                <p>12</p>
            <body>
        </html>
        """
        # act
        result = list(testee.preprocess_single(markup))
        # assert
        assert_that(result, is_(not_(empty())))
