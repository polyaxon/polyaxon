import conf

from options.registry.scheduler import SCHEDULER_GLOBAL_COUNTDOWN

from polyaxon.celery_api import app
from workers.base import PolyaxonTask


app.Task = PolyaxonTask  # Custom base class for logging


def send(task_name, kwargs=None, **options):
    options['ignore_result'] = options.get('ignore_result', True)
    if 'countdown' not in options:
        options['countdown'] = conf.get(SCHEDULER_GLOBAL_COUNTDOWN)
    return app.send_task(task_name, kwargs=kwargs, **options)
