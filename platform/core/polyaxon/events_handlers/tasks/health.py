import workers

from checks import health_task
from polyaxon.settings import EventsCeleryTasks


@workers.app.task(name=EventsCeleryTasks.EVENTS_HEALTH, ignore_result=False)
def events_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
