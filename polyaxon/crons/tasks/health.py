import workers

from checks import health_task
from polyaxon.settings import CronsCeleryTasks


@workers.app.task(name=CronsCeleryTasks.CRONS_HEALTH, ignore_result=False)
def crons_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
