import workers

from checks import health_task
from polyaxon.settings import SchedulerCeleryTasks


@workers.app.task(name=SchedulerCeleryTasks.SCHEDULER_HEALTH, ignore_result=False)
def scheduler_health(x, y):
    return health_task.health_task(x, y)
