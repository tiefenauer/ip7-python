import logging
from abc import abstractmethod

from pony.orm import commit, db_session

from src.database.entities_pg import Semantic_Avg_Classification_Results, Fts_Classification_Results, X28_HTML, \
    Semantic_Rf_Classification_Results, Structural_Classification_NV_Results, Structural_Classification_NVT_Results, \
    Loe_Classification_Result, Combined_Classification_Results

log = logging.getLogger(__name__)


class ClassificationResults(object):
    @db_session
    def __init__(self, Entity):
        self.Entity = Entity

    @db_session
    def update_classification(self, rowid, predicted_class, scores):
        sc_str = scores[0]
        sc_tol = scores[1]
        sc_lin = scores[2]

        job_row = X28_HTML.get(lambda d: d.id == rowid)
        classification_result = self.create_entity(job_row, predicted_class, sc_str, sc_tol, sc_lin)
        commit()
        return classification_result

    @db_session
    def truncate(self):
        log.info('Truncating target tables...')
        self.Entity.select().delete(bulk=True)
        commit()
        log.info('...done!')

    @abstractmethod
    def create_entity(self, job_class, predicted_class, sc_str, sc_tol, sc_lin):
        """return entity class to use for db write"""


class FtsClassificationResults(ClassificationResults):
    def __init__(self):
        super(FtsClassificationResults, self).__init__(Fts_Classification_Results)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Fts_Classification_Results(job=job_entity,
                                          job_name=predicted_class,
                                          score_strict=sc_str,
                                          score_tolerant=sc_tol,
                                          score_linear=sc_lin)


class CombinedClassificatoinResults(ClassificationResults):
    def __init__(self):
        super(CombinedClassificatoinResults, self).__init__(Combined_Classification_Results)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Combined_Classification_Results(job=job_entity,
                                               job_name=predicted_class,
                                               score_strict=sc_str,
                                               score_tolerant=sc_tol,
                                               score_linear=sc_lin)


class SemanticAvgClassificationResults(ClassificationResults):
    def __init__(self):
        super(SemanticAvgClassificationResults, self).__init__(Semantic_Avg_Classification_Results)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Avg_Classification_Results(job=job_entity,
                                                   job_name=predicted_class,
                                                   score_strict=sc_str,
                                                   score_tolerant=sc_tol,
                                                   score_linear=sc_lin)


class SemanticRfClassificationResults(ClassificationResults):
    def __init__(self):
        super(SemanticRfClassificationResults, self).__init__(Semantic_Rf_Classification_Results)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Rf_Classification_Results(job=job_entity,
                                                  job_name=predicted_class,
                                                  score_strict=sc_str,
                                                  score_tolerant=sc_tol,
                                                  score_linear=sc_lin)


class StructuralClassificationNVResults(ClassificationResults):
    def __init__(self):
        super(StructuralClassificationNVResults, self).__init__(Structural_Classification_NV_Results)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Structural_Classification_NV_Results(job=job_entity,
                                                    job_name=predicted_class,
                                                    score_strict=sc_str,
                                                    score_tolerant=sc_tol,
                                                    score_linear=sc_lin)


class StructuralClassificationNVTResults(ClassificationResults):
    def __init__(self):
        super(StructuralClassificationNVTResults, self).__init__(Structural_Classification_NVT_Results)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Structural_Classification_NVT_Results(job=job_entity,
                                                     job_name=predicted_class,
                                                     score_strict=sc_str,
                                                     score_tolerant=sc_tol,
                                                     score_linear=sc_lin)


class LoeClassificationResults(ClassificationResults):

    def __init__(self):
        super(LoeClassificationResults, self).__init__(Loe_Classification_Result)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        workquota_min, workquota_max = predicted_class
        return Loe_Classification_Result(job=job_entity,
                                         workquota_min=workquota_min,
                                         workquota_max=workquota_max,
                                         score_strict=sc_str,
                                         score_tolerant=sc_tol,
                                         score_linear=sc_lin)
