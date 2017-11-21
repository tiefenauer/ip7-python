import numpy

from src.classifier.semantic_classifier import SemanticClassifier


class SemanticClassifierAvg(SemanticClassifier):
    def make_feature_vec(self, words):
        featureVec = numpy.zeros((self.num_features), dtype='float32')
        nwords = 0
        for word in words:
            if word in self.index2word_set:
                nwords += 1
                featureVec = numpy.add(featureVec, self.model[word])
        featureVec = numpy.divide(featureVec, nwords)
        return featureVec

    def title(self):
        return 'Semantic Classifier (average vector)'

    def description(self):
        return """Classifies some text according to semantic criteria. The class is determined by calculating the
               average vector over all words from the text (only indexed words)."""

    def label(self):
        return 'semantic_avg'
