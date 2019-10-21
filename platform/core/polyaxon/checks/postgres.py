from typing import Dict

from django.db import connection

from checks.base import Check
from checks.results import Result


class PostgresCheck(Check):
    @staticmethod
    def pg_health() -> Result:
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1; -- Healthcheck')
                health = cursor.fetchone()[0] == 1
                if health:
                    cursor.execute("select pg_database_size('postgres') as size")
                    size = cursor.fetchone()
                    return Result(message='Service is healthy, db size {}'.format(size))
            return Result(message='Service is not working.', severity=Result.WARNING)
        except Exception as e:
            return Result(message='Service unable to connect, encountered "{}" error.'.format(e),
                          severity=Result.ERROR)

    @classmethod
    def run(cls) -> Dict:
        result = cls.pg_health()
        return {'POSTGRES': result}
