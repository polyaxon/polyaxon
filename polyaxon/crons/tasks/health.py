from checks import health_task
from polyaxon.celery_api import celery_app
from polyaxon.settings import CronsCeleryTasks


@celery_app.task(name=CronsCeleryTasks.CRONS_HEALTH, ignore_result=False)
def crons_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
