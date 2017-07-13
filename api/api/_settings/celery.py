# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config


BROKER_TRANSPORT = 'redis'
BROKER_URL = config.get_string('REDIS_CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config.get_string('REDIS_CELERY_RESULT_BACKEND')

CELERY_ALWAYS_EAGER = config.get_boolean('CELERY_ALWAYS_EAGER')
if CELERY_ALWAYS_EAGER:
    BROKER_TRANSPORT = 'memory'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


class CeleryTasks(object):
    START_EXPERIMENT = 'start_xp'


class CeleryQueues(object):
    EXPERIMENTS = 'api.xps'


CELERY_ROUTES = {
    CeleryTasks.START_EXPERIMENT: {'queue': CeleryQueues.EXPERIMENTS},
}
