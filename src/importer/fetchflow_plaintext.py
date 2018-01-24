from pony.orm import commit, db_session
from tqdm import tqdm

from src.database.entities_pg import Fetchflow_HTML
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor

preprocessor = RelevantTagsPreprocessor()

with db_session:
    query = Fetchflow_HTML.select(lambda row: row.preprocessed is None or row.preprocessed == False)
    count = query.count()
    for i in tqdm(range(count), unit=' rows'):
        row = query[i:(i + 1)][0]
        tags = preprocessor.preprocess_single(row)
        tags = list(tags)
        plaintext = '\n'.join(tag.getText() for tag in tags)
        row.plaintext = plaintext
        row.preprocessed = True
        commit()
