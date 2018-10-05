from django.db import connection

from checks.base import Check
from checks.results import Result


class PostgresCheck(Check):
    @staticmethod
    def pg_health():
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1; -- Healthcheck')
            health = cursor.fetchone()[0] == 1
            size = None
            if health:
                cursor.execute("select pg_database_size('postgres') as size")
                size = cursor.fetchone()
        return health, size

    @classmethod
    def run(cls):
        health, size = cls.pg_health()
        if health:
            result = Result(message='Service is healthy, db size {}'.format(size))
        else:
            result = Result(message='Service is not working.', severity=Result.ERROR)

        return {'POSTGRES': result}
