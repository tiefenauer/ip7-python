import logging
import sys
from abc import abstractmethod

from pony.orm import commit, db_session

from src.database.entities_x28 import Semantic_Avg_Classification_Results, Classification_Results, \
    Fts_Classification_Results, Data_Train

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ClassificationResults(object):
    @db_session
    def __init__(self, method, args):
        self.classification_method = method
        self.write = args.write if hasattr(args, 'write') else False
        if hasattr(args, 'truncate') and args.truncate:
            logging.info('truncating target tables...')
            Classification_Results.select(lambda r: r.clf_method == self.classification_method).delete()
            commit()

    @db_session
    def update_classification(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        if not self.write or not predicted_class:
            # do not write results if dry run or class could not be predicted
            return
        job_class = Data_Train.get(lambda d: d.id == job_class.id)
        classification_result = self.create_entity(job_class, predicted_class, sc_str, sc_tol, sc_lin)
        commit()
        return classification_result

    @abstractmethod
    def create_entity(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        """return entity class to use for db write"""


class FtsClassificationResults(ClassificationResults):
    def __init__(self, args):
        super(FtsClassificationResults, self).__init__('fts', args)

    def create_entity(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        return Fts_Classification_Results(job_class=job_class,
                                          job_name=predicted_class,
                                          score_strict=sc_str,
                                          score_tolerant=sc_tol,
                                          score_linear=sc_lin)


class SemanticAvgClassificationResults(ClassificationResults):
    def __init__(self, args):
        super(SemanticAvgClassificationResults, self).__init__('semantic_avg', args)

    def create_entity(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Avg_Classification_Results(job_class=job_class,
                                                   job_name=predicted_class,
                                                   score_strict=sc_str,
                                                   score_tolerant=sc_tol,
                                                   score_linear=sc_lin)
