from checks import health_task
from polyaxon.celery_api import celery_app
from polyaxon.settings import K8SEventsCeleryTasks


@celery_app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HEALTH, ignore_result=False)
def k8s_events_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
