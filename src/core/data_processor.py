from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """a data processor is something that finds information in data"""

    def __init__(self, args, preprocessor):
        self.preprocessor = preprocessor

    def process(self, raw_data):
        num_rows = raw_data.num_rows if hasattr(raw_data, 'num_rows') else -1
        processed_data = self.preprocessor.preprocess(raw_data, num_rows)
        self._process(processed_data)

    @abstractmethod
    def _process(self, processed_data):
        """process an iterable dataset yielding the processing result for each item"""

    @abstractmethod
    def title(self):
        """a short title of the classification strategy"""
        return

    @abstractmethod
    def description(self):
        """describe how the classification is done"""
        return

    @abstractmethod
    def label(self):
        """short label for visualisation"""
        return
