from src.classifier.structural_classifier import StructuralClassifier
from src.database.X28_Data_Train import X28_Data_Train
from src.preprocessing.preprocessor_structural import StructuralX28Preprocessor
from src.util.boot_util import set_up_logger, parse_args

logging = set_up_logger()
args = parse_args()

data_train = X28_Data_Train(args)
preprocessor = StructuralX28Preprocessor()
classifier = StructuralClassifier()

if __name__ == '__main__':
    rows_processed = preprocessor.preprocess(data_train, data_train.num_rows)
    classifier.train_model(rows_processed)
    # tagged_sents = list(brown.tagged_sents(categories='news'))
    # print(len(tagged_sents))
