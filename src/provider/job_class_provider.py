from src import db
from src.db import Database


class JobClassProvider(object):
    def __enter__(self):
        self.conn = db.connect_to(Database.X28_PG)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def __iter__(self):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, job_class, job_class_stem FROM job_classes""")
        for row in cursor:
            yield {
                'id': row['id'],
                'job_class': row['job_class'],
                'job_class_stem': row['job_class_stem']}

    def get_job_class_by_name(self, job_name):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, job_class, job_class_stem FROM job_classes WHERE job_class = %s""", [job_name])
        return cursor.fetchone()

    def get_variants_by_name(self, job_name):
        cursor = self.conn.cursor()
        cursor.execute("""
        select v.id, v.job_class_variant
        from job_classes_variants v
        join job_classes c on c.id = v.job_class_id
        where c.job_class = %s
        """, [job_name])
        return cursor.fetchall()

    def get_variants_by_id(self, job_id):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT v.id, v.job_class_variant
        FROM job_classes_variants v
        JOIN job_classes c ON c.id = v.job_class_id
        WHERE c.id = %s
        """, [job_id])
        return cursor.fetchall()
