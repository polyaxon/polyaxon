from checks.worker import WorkerCheck
from polyaxon.config_settings import K8SEventsCeleryTasks


class EventsCheck(WorkerCheck):
    WORKER_HEALTH_TASK = K8SEventsCeleryTasks.K8S_EVENTS_HEALTH
    WORKER_NAME = 'EVENTS'
