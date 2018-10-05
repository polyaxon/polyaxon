from checks import health_task
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import HPCeleryTasks


@celery_app.task(name=HPCeleryTasks.HP_HEALTH, ignore_result=False)
def hp_heath(x, y):
    return health_task.health_task(x, y)
