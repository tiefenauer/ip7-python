import unittest
from unittest.mock import MagicMock

from mysql.connector import MySQLConnection

from src import job_importer


class TestImporter(unittest.TestCase):
    def test_import_jobs_returns_iterable(self):
        # arrange
        conn = MySQLConnection()
        conn.cursor = MagicMock(name='cursor')
        # act
        result = job_importer.import_all(conn)
        # assert
