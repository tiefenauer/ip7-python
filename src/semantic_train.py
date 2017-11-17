from src.classifier.semantic_classifier import SemanticClassifier
from src.database.X28_Data_Train import X28_Data_Train
from src.preprocessing.preprocessor_semantic import SemanticX28Preprocessor
from src.util.boot_util import parse_args, set_up_logger

logging = set_up_logger()
args = parse_args()


class MySentences(object):
    def __init__(self, rows):
        self.rows = rows

    def __iter__(self):
        for sentences in self.rows:
            yield sentences


data_train = X28_Data_Train(args)
preprocessor = SemanticX28Preprocessor(remove_stopwords=False)  # do not remove stopwords for training!
classifier = SemanticClassifier(args.model)

if __name__ == '__main__':
    rows_processed = preprocessor.preprocess(data_train, data_train.num_rows)
    rows = (row.processed for row in rows_processed)
    classifier.train_model(MySentences(rows))
