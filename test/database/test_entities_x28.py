import unittest

from src.database.entities_pg import Job_Class, Job_Class_To_Job_Class_Similar, Job_Class_Similar, X28_HTML, \
    Job_Class_Variant, Classification_Results


class TestEntitiesX28(unittest.TestCase):
    def test_entities_are_correctly_mapped(self):
        X28_HTML.select()
        Job_Class.select()
        Job_Class_To_Job_Class_Similar.select()
        Job_Class_Similar.select()
        Job_Class_Variant.select()
        Classification_Results.select()