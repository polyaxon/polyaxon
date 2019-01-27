from checks import health_task
from polyaxon.celery_api import celery_app
from polyaxon.settings import EventsCeleryTasks


@celery_app.task(name=EventsCeleryTasks.EVENTS_HEALTH, ignore_result=False)
def events_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
