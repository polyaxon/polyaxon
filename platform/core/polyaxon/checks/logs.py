from checks.worker import WorkerCheck
from polyaxon.config_settings import LogsCeleryTasks


class LogsCheck(WorkerCheck):
    WORKER_HEALTH_TASK = LogsCeleryTasks.LOGS_HEALTH
    WORKER_NAME = 'LOGS'
