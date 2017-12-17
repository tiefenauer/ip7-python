from pony.orm import db_session, commit
from tqdm import tqdm

from src.database.entities_pg import X28_HTML
from src.preprocessing import preproc
from src.preprocessing.relevant_tags_preprocessor import RelevantTagsPreprocessor


def to_sentences(tag):
    for sent in preproc.to_sentences(tag.getText()):
        yield tag.name, sent


preprocessor = RelevantTagsPreprocessor()
with db_session:
    query = X28_HTML.select()
    for row in tqdm(query, total=query.count(), unit=' rows'):
        tags = preprocessor.preprocess_single(row)
        sentences = ''
        for tag in tags:
            for tag_name, sent in to_sentences(tag):
                sentences += tag_name + '##' + sent + '\n'
        row.sentences = sentences
        commit()
