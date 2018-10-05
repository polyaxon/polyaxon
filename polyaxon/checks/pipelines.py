from checks.worker import WorkerCheck
from polyaxon.config_settings import PipelinesCeleryTasks


class PipelinesCheck(WorkerCheck):
    WORKER_HEALTH_TASK = PipelinesCeleryTasks.PIPELINES_HEALTH
    WORKER_NAME = 'PIPELINES'
