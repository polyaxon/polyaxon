from typing import Dict

import psutil

from checks.base import Check
from checks.results import Result


class DiskCheck(Check):
    WARNING_THRESHOLD = 10
    ERROR_THRESHOLD = 10
    HOST = None

    @classmethod
    def run(cls) -> Dict:
        try:
            disk = psutil.disk_usage('/')
            if disk.percent >= cls.ERROR_THRESHOLD:
                result = Result(
                    message='{host} {percent}% disk usage exceeds error {disk_usage}%'.format(
                        host=cls.HOST, percent=disk.percent, disk_usage=cls.ERROR_THRESHOLD),
                    severity=Result.ERROR
                )
            elif disk.percent >= cls.WARNING_THRESHOLD:
                result = Result(
                    message='{host} {percent}% disk usage exceeds warning {disk_usage}%'.format(
                        host=cls.HOST, percent=disk.percent, disk_usage=cls.ERROR_THRESHOLD),
                    severity=Result.ERROR
                )
            else:
                result = Result()
        except ValueError:
            result = Result(
                message='An error was raised, try again later.',
                severity=Result.ERROR
            )
        return {'DISK': result}
