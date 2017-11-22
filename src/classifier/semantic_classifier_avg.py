import numpy
from sklearn.ensemble import RandomForestClassifier

from src.classifier.semantic_classifier import SemanticClassifier


class SemanticClassifierAvg(SemanticClassifier):
    def getAvgFeatureVecs(self, data, num_rows):
        counter = 0
        avgFeatureVecs = numpy.zeros((num_rows, self.num_features), dtype="float32")
        for row in data:
            if counter % 1000 == 0:
                print("Review {} of {}".format(counter, num_rows))
            avgFeatureVecs[counter] = self.make_feature_vec(row.processed)
            counter += 1
        return avgFeatureVecs

    def make_feature_vec(self, words):
        featureVec = numpy.zeros((self.num_features), dtype='float32')
        nwords = 0
        for word in words:
            if word in self.index2word_set:
                nwords += 1
                featureVec = numpy.add(featureVec, self.model[word])
        if nwords > 0:
            featureVec = numpy.divide(featureVec, nwords)
        return featureVec

    def title(self):
        return 'Semantic Classifier (average vector)'

    def description(self):
        return """Classifies some text according to semantic criteria. The class is determined by calculating the
               average vector over all words from the text (only indexed words)."""

    def label(self):
        return 'semantic_avg'
