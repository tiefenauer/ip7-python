from src.database.X28_Data_Train import X28_Data_Train
from src.preprocessing.preprocessor_structural import StructuralX28Preprocessor
from src.util.boot_util import set_up_logger, parse_args

logging = set_up_logger()
args = parse_args()

data_train = X28_Data_Train(args)
preprocessor = StructuralX28Preprocessor()

if __name__ == '__main__':
    rows_processed = preprocessor.preprocess(data_train)
