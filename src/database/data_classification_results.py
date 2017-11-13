import logging
import sys

from pony.orm import commit, db_session

from src.database.entities import Classification_Results, Data_Train

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ClassificationResults(object):
    def __init__(self, clf_method, args):
        self.clf_method = clf_method
        self.write = args.write if hasattr(args, 'write') else False
        self.truncate = args.truncate if hasattr(args, 'truncate') else False

    def __enter__(self):
        if self.truncate:
            self.truncate_classification_tables()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @db_session
    def update_classification(self, id, predicted_class, sc_str, sc_tol, sc_lin):
        if not (self.write and predicted_class):
            # do not write classification if only dry run or no predicted class
            return
        job_class = Data_Train.get(id=id)
        classification_result = Classification_Results(clf_method=self.clf_method,
                                                       job_class=job_class,
                                                       job_name=predicted_class,
                                                       score_strict=sc_str,
                                                       score_tolerant=sc_tol,
                                                       score_linear=sc_lin
                                                       )
        commit()
        return classification_result

    @db_session
    def truncate_classification_tables(self):
        logging.info('truncating target tables...')
        Classification_Results.select(lambda r: r.clf_method == self.clf_method).delete()
        commit()
