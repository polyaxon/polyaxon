from typing import Dict

import psutil

from checks.base import Check
from checks.results import Result


class MemoryCheck(Check):
    WARNING_THRESHOLD = 10
    ERROR_THRESHOLD = 10
    HOST = None

    @classmethod
    def run(cls) -> Dict:
        try:
            memory = psutil.virtual_memory()
            available = '{:n}'.format(int(memory.available / 1024 / 1024))
            if memory.available < (cls.ERROR_THRESHOLD * 1024 * 1024):
                result = Result(
                    message='Memory available ({}) is below error threshold ({})'.format(
                        available, cls.ERROR_THRESHOLD),
                    severity=Result.ERROR
                )
            elif memory.available < (cls.ERROR_THRESHOLD * 1024 * 1024):
                result = Result(
                    message='Memory available ({}) is below warning threshold ({})'.format(
                        available, cls.WARNING_THRESHOLD),
                    severity=Result.WARNING
                )
            else:
                result = Result()
        except ValueError:
            result = Result(
                message='An error was raised, try again later.',
                severity=Result.ERROR
            )
        return {'MEMORY': result}
