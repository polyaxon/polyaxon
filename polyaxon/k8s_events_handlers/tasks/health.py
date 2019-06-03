import workers

from checks import health_task
from polyaxon.settings import K8SEventsCeleryTasks


@workers.app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HEALTH, ignore_result=False)
def k8s_events_health(x: int, y: int) -> int:
    return health_task.health_task(x, y)
