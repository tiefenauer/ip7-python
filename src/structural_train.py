from src.classifier.structural_classifier import StructuralClassifier
from src.database.X28TestData import X28TestData
from src.preprocessing.preprocessor_structural import StructuralX28Preprocessor
from src.util.boot_util import log_setup, parse_args

logging = log_setup()
args = parse_args()

data_train = X28TestData(args)
preprocessor = StructuralX28Preprocessor()
classifier = StructuralClassifier()

if __name__ == '__main__':
    rows_processed = preprocessor.preprocess(data_train, data_train.num_rows)
    classifier.train_model(rows_processed)
    # tagged_sents = list(brown.tagged_sents(categories='news'))
    # print(len(tagged_sents))
