import logging
import sys
from abc import abstractmethod

from pony.orm import commit, db_session

from src.database.entities_pg import Semantic_Avg_Classification_Results, Classification_Results, \
    Fts_Classification_Results, X28_HTML

logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class ClassificationResults(object):
    @db_session
    def __init__(self, method, Entity, args):
        self.classification_method = method
        self.Entity = Entity
        self.write = args.write if hasattr(args, 'write') else False
        if hasattr(args, 'truncate') and args.truncate:
            logging.info('truncating target tables...')
            Classification_Results.select(lambda r: r.clf_method == self.classification_method).delete()
            commit()

    @db_session
    def update_classification(self, entity, predicted_class, sc_str, sc_tol, sc_lin):
        if not self.write or not predicted_class:
            # do not write results if dry run or class could not be predicted
            return
        job_row = X28_HTML.get(lambda d: d.id == entity.id)
        classification_result = self.create_entity(job_row, predicted_class, sc_str, sc_tol, sc_lin)
        commit()
        return classification_result

    @db_session
    def truncate(self):
        self.Entity.select().delete()

    @abstractmethod
    def create_entity(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        """return entity class to use for db write"""


class FtsClassificationResults(ClassificationResults):
    def __init__(self, args):
        super(FtsClassificationResults, self).__init__('fts', Fts_Classification_Results, args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Fts_Classification_Results(job=job_entity,
                                          job_name=predicted_class,
                                          score_strict=sc_str,
                                          score_tolerant=sc_tol,
                                          score_linear=sc_lin)


class SemanticAvgClassificationResults(ClassificationResults):
    def __init__(self, args):
        super(SemanticAvgClassificationResults, self).__init__('semantic_avg', Semantic_Avg_Classification_Results,
                                                               args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Avg_Classification_Results(job=job_entity,
                                                   job_name=predicted_class,
                                                   score_strict=sc_str,
                                                   score_tolerant=sc_tol,
                                                   score_linear=sc_lin)
