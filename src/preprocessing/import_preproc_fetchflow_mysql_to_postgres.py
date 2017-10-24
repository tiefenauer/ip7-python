from src.importer.fetchflow_importer import FetchflowImporter
from src.importer.x28_importer import X28Importer
from src.preproc import preprocess

if __name__ == '__main__':
    with FetchflowImporter() as fetchflow, X28Importer() as x28_importer:
        x28_importer.truncate_fetchflow()
        for (fetchflow_id, dom) in ((row['id'], row['dom']) for row in fetchflow if row['dom']):
            result = preprocess(dom)
            x28_importer.insert_fetchflow(fetchflow_id, result)