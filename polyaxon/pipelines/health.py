import workers

from checks import health_task
from polyaxon.settings import PipelinesCeleryTasks


@workers.app.task(name=PipelinesCeleryTasks.PIPELINES_HEALTH, ignore_result=False)
def pipelines_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
