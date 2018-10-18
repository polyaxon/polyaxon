from checks import health_task
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import LogsCeleryTasks


@celery_app.task(name=LogsCeleryTasks.LOGS_HEALTH, ignore_result=False)
def logs_health(x, y):
    return health_task.health_task(x, y)
