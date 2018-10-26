from checks.worker import WorkerCheck
from polyaxon.settings import K8SEventsCeleryTasks


class K8SEventsCheck(WorkerCheck):
    WORKER_HEALTH_TASK = K8SEventsCeleryTasks.K8S_EVENTS_HEALTH
    WORKER_NAME = 'K8SEVENTS'
