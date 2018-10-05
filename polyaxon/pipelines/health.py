from checks import health_task
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import PipelinesCeleryTasks


@celery_app.task(name=PipelinesCeleryTasks.PIPELINES_HEALTH, ignore_result=False)
def pipelines_heath(x, y):
    return health_task.health_task(x, y)
