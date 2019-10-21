import workers

from checks import health_task
from polyaxon.settings import HPCeleryTasks


@workers.app.task(name=HPCeleryTasks.HP_HEALTH, ignore_result=False)
def hp_health(x, y):
    return health_task.health_task(x, y)
