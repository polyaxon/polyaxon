import workers

from checks import health_task
from polyaxon.settings import LogsCeleryTasks


@workers.app.task(name=LogsCeleryTasks.LOGS_HEALTH, ignore_result=False)
def logs_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
