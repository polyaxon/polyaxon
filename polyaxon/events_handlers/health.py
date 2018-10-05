from checks import health_task
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks


@celery_app.task(name=EventsCeleryTasks.EVENTS_HEALTH, ignore_result=False)
def events_heath(x, y):
    return health_task.health_task(x, y)
