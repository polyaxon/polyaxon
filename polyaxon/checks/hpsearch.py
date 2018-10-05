from checks.worker import WorkerCheck
from polyaxon.config_settings import HPCeleryTasks


class HPSearchCheck(WorkerCheck):
    WORKER_HEALTH_TASK = HPCeleryTasks.HP_HEALTH
    WORKER_NAME = 'HPSEARCH'
