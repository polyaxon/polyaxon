import random

from django.conf import settings

from checks.base import Check
from checks.health_task import health_task
from checks.results import Result
from polyaxon.celery_api import app as celery_app


class WorkerCheck(Check):
    HEALTH_CHECK_TIMEOUT = settings.HEALTH_CHECK_WORKER_TIMEOUT
    WORKER_HEALTH_TASK = None
    WORKER_NAME = None

    @classmethod
    def run(cls):
        arg = random.randint(1, 10)
        result = None
        try:
            task_result = celery_app.send_task(
                cls.WORKER_HEALTH_TASK,
                args=[arg, arg],
                expires=cls.HEALTH_CHECK_TIMEOUT,
            )
            task_result.get(timeout=cls.HEALTH_CHECK_TIMEOUT)
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
