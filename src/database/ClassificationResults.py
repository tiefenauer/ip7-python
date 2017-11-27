import logging
from abc import abstractmethod

from pony.orm import commit, db_session

from src.database.entities_pg import Semantic_Avg_Classification_Results, Fts_Classification_Results, X28_HTML, \
    Semantic_Rf_Classification_Results, Structural_Classification_NV_Results, Structural_Classification_NVT_Results

log = logging.getLogger(__name__)


class ClassificationResults(object):
    @db_session
    def __init__(self, classifier, Entity, args):
        self.classification_method = classifier.label()
        self.Entity = Entity
        self.write = args.write if hasattr(args, 'write') else False
        if hasattr(args, 'truncate') and args.truncate:
            log.info('truncating target tables...')
            self.truncate()
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
    def __init__(self, args, classifier):
        super(FtsClassificationResults, self).__init__(classifier, Fts_Classification_Results, args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Fts_Classification_Results(job=job_entity,
                                          job_name=predicted_class,
                                          score_strict=sc_str,
                                          score_tolerant=sc_tol,
                                          score_linear=sc_lin)


class SemanticAvgClassificationResults(ClassificationResults):
    def __init__(self, args, classifier):
        super(SemanticAvgClassificationResults, self).__init__(classifier, Semantic_Avg_Classification_Results, args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Avg_Classification_Results(job=job_entity,
                                                   job_name=predicted_class,
                                                   score_strict=sc_str,
                                                   score_tolerant=sc_tol,
                                                   score_linear=sc_lin)


class SemanticRfClassificationResults(ClassificationResults):
    def __init__(self, args, classifier):
        super(SemanticRfClassificationResults, self).__init__(classifier, Semantic_Rf_Classification_Results, args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Semantic_Rf_Classification_Results(job=job_entity,
                                                  job_name=predicted_class,
                                                  score_strict=sc_str,
                                                  score_tolerant=sc_tol,
                                                  score_linear=sc_lin)


class StructuralClassificationNVResults(ClassificationResults):
    def __init__(self, args, classifier):
        super(StructuralClassificationNVResults, self).__init__(classifier, Structural_Classification_NV_Results, args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Structural_Classification_NV_Results(job=job_entity,
                                                    job_name=predicted_class,
                                                    score_strict=sc_str,
                                                    score_tolerant=sc_tol,
                                                    score_linear=sc_lin)


class StructuralClassificationNVTResults(ClassificationResults):
    def __init__(self, args, classifier):
        super(StructuralClassificationNVTResults, self).__init__(classifier, Structural_Classification_NVT_Results,
                                                                 args)

    def create_entity(self, job_entity, predicted_class, sc_str, sc_tol, sc_lin):
        return Structural_Classification_NVT_Results(job=job_entity,
                                                     job_name=predicted_class,
                                                     score_strict=sc_str,
                                                     score_tolerant=sc_tol,
                                                     score_linear=sc_lin)
