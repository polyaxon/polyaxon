import random

from typing import Dict

import conf

from checks.base import Check
from checks.health_task import health_task
from checks.results import Result
from polyaxon.celery_api import celery_app


class WorkerCheck(Check):
    WORKER_HEALTH_TASK = None
    WORKER_NAME = None

    @classmethod
    def run(cls) -> Dict:
        timeout = conf.get('HEALTH_CHECK_WORKER_TIMEOUT')
        arg = random.randint(1, 10)
        result = None
        try:
            task_result = celery_app.send_task(
                cls.WORKER_HEALTH_TASK,
                args=[arg, arg],
                expires=timeout,
            )
            task_result.get(timeout=timeout)
            if task_result.result != health_task(arg, arg):
                result = Result(
                    message='Service returned wrong health result.',
                    severity=Result.WARNING
                )
        except IOError:
            result = Result(
                message='Service has an "IOError".',
                severity=Result.ERROR
            )
        except Exception as e:
            result = Result(
                message='Service has an "{}" error.'.format(e),
                severity=Result.ERROR
            )
        if not result:
            result = Result()

        return {cls.WORKER_NAME: result}
