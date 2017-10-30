import unittest

from src.evaluation.evaluation import Evaluation


class TestEvaluationPlotter(unittest.TestCase):
    def test_plot_some_results(self):
        # arrange
        evaluators = []
        testee = Evaluation(evaluators)
        # act
        testee.update()
