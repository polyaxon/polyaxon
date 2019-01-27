from checks import health_task
from polyaxon.celery_api import celery_app
from polyaxon.settings import PipelinesCeleryTasks


@celery_app.task(name=PipelinesCeleryTasks.PIPELINES_HEALTH, ignore_result=False)
def pipelines_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
