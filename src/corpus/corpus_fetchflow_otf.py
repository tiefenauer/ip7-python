from tqdm import tqdm

from src.database.fetchflow_data import FetchflowData
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor
from src.preprocessing.semantic_preprocessor import SemanticPreprocessor
from test.testutils import create_dummy_row


class FetchflowOTFCorpus(object):
    """Iterator class for corpus for Fetchflow-Vacancies. The corpus contains a list of sentences whereas each
    sentence comes from a vacancy and is read from the DB and preprocessed on-the-fly
    """

    def __init__(self, row_id=None):
        self.row_id = row_id

    def __iter__(self):
        fetchflow_rows = FetchflowData(self.row_id)
        relevant_tags_preprocessor = RelevantTagsPreprocessor(fetchflow_rows, include_title=False)
        semantic_preprocessor = SemanticPreprocessor(fetchflow_rows)
        for fetchflow_row in tqdm(fetchflow_rows, unit=' rows'):
            row = create_dummy_row(html=fetchflow_row.html)
            tags = relevant_tags_preprocessor.preprocess_single(row)
            plaintext = '\n'.join(tag.getText() for tag in tags)
            row.plaintext = plaintext
            for sentence in semantic_preprocessor.preprocess_single(row):
                if len(sentence) > 1:
                    yield sentence
