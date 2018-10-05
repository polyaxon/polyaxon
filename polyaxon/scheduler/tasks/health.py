from checks import health_task
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks


@celery_app.task(name=SchedulerCeleryTasks.SCHEDULER_HEALTH, ignore_result=False)
def scheduler_heath(x, y):
    return health_task.health_task(x, y)
