import logging
from abc import abstractmethod

from pony.orm import commit, db_session

from src.database.entities_pg import Semantic_Avg_Classification_Results, Fts_Classification_Results, X28_HTML, \
    Semantic_Rf_Classification_Results, Structural_Classification_NV_Results, Structural_Classification_NVT_Results

log = logging.getLogger(__name__)


class ClassificationResults(object):
    @db_session
    def __init__(self, Entity):
        self.Entity = Entity

    @db_session
    def update_classification(self, entity, predicted_class, sc_str, sc_tol, sc_lin):
        job_row = X28_HTML.get(lambda d: d.id == entity.id)
        classification_result = self.create_entity(job_row, predicted_class, sc_str, sc_tol, sc_lin)
        commit()
        return classification_result

    @db_session
    def truncate(self):
        self.Entity.select().delete(bulk=True)
        commit()

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
