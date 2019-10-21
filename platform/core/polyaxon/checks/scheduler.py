from checks.worker import WorkerCheck
from polyaxon.config_settings import SchedulerCeleryTasks


class SchedulerCheck(WorkerCheck):
    WORKER_HEALTH_TASK = SchedulerCeleryTasks.SCHEDULER_HEALTH
    WORKER_NAME = 'SCHEDULER'
