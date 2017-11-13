from src.database.data_fetchflow import FetchflowImporter
from src.database.data_preprocessed import PreprocessedData
from src.preproc import preprocess

if __name__ == '__main__':
    with FetchflowImporter() as fetchflow, PreprocessedData() as preprocessed_data:
        preprocessed_data.truncate_fetchflow()
        for (fetchflow_id, dom) in ((row['id'], row['dom']) for row in fetchflow if row['dom']):
            result = preprocess(dom)
            preprocessed_data.insert(fetchflow_id, result)
