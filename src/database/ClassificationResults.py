import logging
from abc import abstractmethod

from pony.orm import commit, db_session

from src.database.entities_pg import Semantic_Classification_Results, Fts_Classification_Results, \
    Structural_Classification_Results, \
    Loe_Classification_Result, Combined_Classification_Results

log = logging.getLogger(__name__)


class ClassificationResults(object):
    @db_session
    def __init__(self, Entity):
        self.Entity = Entity

    @db_session
    def update_classification(self, row, predicted_class, scores):
        sc_str = scores[0]
        sc_tol = scores[1]
        sc_lin = scores[2]

        predicted_class = predicted_class or ''

        classification_result = self.create_entity(row.id, predicted_class[:255], sc_str, sc_tol, sc_lin)
        commit()
        return classification_result

    @db_session
    def truncate(self):
        log.info("""Truncating target table {}.clf_method='{}' ...""".format(self.Entity._table_,
                                                                             self.Entity._discriminator_))
        self.Entity.select().delete(bulk=True)
        commit()
        log.info('...done!')

    @abstractmethod
    def create_entity(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        """return entity class to use for db write"""


class FtsClassificationResults(ClassificationResults):
    def __init__(self):
        super(FtsClassificationResults, self).__init__(Fts_Classification_Results)

    def create_entity(self, x28_id, predicted_class, sc_str, sc_tol, sc_lin):
        return Fts_Classification_Results(x28_row=x28_id,
                                          job_name=predicted_class,
                                          score_strict=sc_str,
                                          score_tolerant=sc_tol,
                                          score_linear=sc_lin)


class CombinedClassificationResults(ClassificationResults):
    def __init__(self):
        super(CombinedClassificationResults, self).__init__(Combined_Classification_Results)

    def create_entity(self, x28_id, predicted_class, sc_str, sc_tol, sc_lin):
        return Combined_Classification_Results(x28_row=x28_id,
                                               job_name=predicted_class,
                                               score_strict=sc_str,
                                               score_tolerant=sc_tol,
                                               score_linear=sc_lin)


class SemanticAvgClassificationResults(ClassificationResults):
    def __init__(self):
        super(SemanticAvgClassificationResults, self).__init__(Semantic_Classification_Results)

    def create_entity(self, x28_id, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Classification_Results(x28_row=x28_id,
                                               job_name=predicted_class,
                                               score_strict=sc_str,
                                               score_tolerant=sc_tol,
                                               score_linear=sc_lin)


class StructuralClassificationResults(ClassificationResults):
    def __init__(self):
        super(StructuralClassificationResults, self).__init__(Structural_Classification_Results)

    def create_entity(self, x28_id, predicted_class, sc_str, sc_tol, sc_lin):
        return Structural_Classification_Results(x28_row=x28_id,
                                                 job_name=predicted_class,
                                                 score_strict=sc_str,
                                                 score_tolerant=sc_tol,
                                                 score_linear=sc_lin)


class LoeClassificationResults(ClassificationResults):

    def __init__(self):
        super(LoeClassificationResults, self).__init__(Loe_Classification_Result)

    def create_entity(self, x28_id, predicted_class, sc_str, sc_tol, sc_lin):
        workquota_min, workquota_max = predicted_class
        return Loe_Classification_Result(x28_row=x28_id,
                                         workquota_min=workquota_min,
                                         workquota_max=workquota_max,
                                         score_strict=sc_str,
                                         score_tolerant=sc_tol,
                                         score_linear=sc_lin)
