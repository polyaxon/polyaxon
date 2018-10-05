from checks.worker import WorkerCheck
from polyaxon.config_settings import CronsCeleryTasks


class CronsCheck(WorkerCheck):
    WORKER_HEALTH_TASK = CronsCeleryTasks.CRONS_HEALTH
    WORKER_NAME = 'CRONS'
