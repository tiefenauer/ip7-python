from src.classifier.semantic_classifier import SemanticClassifier


class SemanticClassifierAvg(SemanticClassifier):
    def classify(self, processed_row):
        feature_vec = self.to_average_vector(processed_row)
        # query w2v model
        top10 = self.model.similar_by_vector(feature_vec, 1)
        if top10:
            return next(iter(top10))[0]
        return None

    def title(self):
        return 'Semantic Classifier (average vector)'

    def description(self):
        return """Classifies some text according to semantic criteria. The class is determined by calculating the
               average vector over all words from the text (only indexed words)."""

    def label(self):
        return 'semantic_avg'
