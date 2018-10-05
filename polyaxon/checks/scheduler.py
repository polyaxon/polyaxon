from checks.worker import WorkerCheck
from polyaxon.config_settings import SchedulerCeleryTasks


class EventsCheck(WorkerCheck):
    WORKER_HEALTH_TASK = SchedulerCeleryTasks.SCHEDULER_HEALTH
    WORKER_NAME = 'SCHEDULER'
