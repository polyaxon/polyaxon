# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config

CELERY_TRACK_STARTED = True

BROKER_URL = config.get_string('AMQP_CELERY_BROKER_URL')

CELERY_RESULT_BACKEND = config.get_string('REDIS_CELERY_RESULT_BACKEND')
CELERYD_PREFETCH_MULTIPLIER = config.get_int("CELERYD_PREFETCH_MULTIPLIER")

CELERY_ALWAYS_EAGER = config.get_boolean('CELERY_ALWAYS_EAGER')
if CELERY_ALWAYS_EAGER:
    BROKER_TRANSPORT = 'memory'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Constants
EXPERIMENTS_SCHEDULER_INTERVAL_SEC = config.get_int('EXPERIMENTS_SCHEDULER_INTERVAL_SEC',
                                                    is_optional=True) or 30


class CeleryTasks(object):
    START_EXPERIMENT = 'start_experiment'
    START_EXPERIMENTS = 'start_experiments'


class CeleryQueues(object):
    EXPERIMENTS = 'api.experiments'


CELERY_ROUTES = {
    CeleryTasks.START_EXPERIMENT: {'queue': CeleryQueues.EXPERIMENTS},
    CeleryTasks.START_EXPERIMENTS: {'queue': CeleryQueues.EXPERIMENTS},
}
