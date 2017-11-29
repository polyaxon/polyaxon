# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from datetime import timedelta

from kombu import Exchange, Queue

from api.utils import config

CELERY_TRACK_STARTED = True

CELERY_BROKER_URL = config.get_string('POLYAXON_AMQP_URL')
INTERNAL_EXCHANGE = config.get_string('POLYAXON_INTERNAL_EXCHANGE')

CELERY_RESULT_BACKEND = config.get_string('POLYAXON_REDIS_CELERY_RESULT_BACKEND_URL')
CELERYD_PREFETCH_MULTIPLIER = config.get_int("POLYAXON_CELERYD_PREFETCH_MULTIPLIER")

CELERY_ALWAYS_EAGER = config.get_boolean('POLYAXON_CELERY_ALWAYS_EAGER')
if CELERY_ALWAYS_EAGER:
    BROKER_TRANSPORT = 'memory'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


class Intervals(object):
    """All intervals are in seconds"""
    EXPERIMENTS_SCHEDULER = config.get_int(
        'POLYAXON_INTERVALS_EXPERIMENTS_SCHEDULER', is_optional=True) or 30
    CLUSTERS_UPDATE_SYSTEM_INFO = config.get_int(
        'POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_INFO',
        is_optional=True) or 150
    CLUSTERS_UPDATE_SYSTEM_NODES = config.get_int(
        'POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_NODES',
        is_optional=True) or 150

    @staticmethod
    def get_schedule(interval):
        return timedelta(seconds=int(interval))

    @staticmethod
    def get_expires(interval):
        int(interval / 2)


class RoutingKeys(object):
    EVENTS_NAMESPACE = config.get_string('POLYAXON_ROUTING_KEYS_EVENTS_NAMESPACE')
    EVENTS_RESOURCES = config.get_string('POLYAXON_ROUTING_KEYS_EVENTS_RESOURCES')
    EVENTS_JOB_STATUSES = config.get_string('POLYAXON_ROUTING_KEYS_EVENTS_JOB_STATUSES')
    LOGS_SIDECARS = config.get_string('POLYAXON_ROUTING_KEYS_LOGS_SIDECARS')


class CeleryRoutedTasks(object):
    """Tasks that handles exchanges messages."""
    EVENTS_NAMESPACE = RoutingKeys.EVENTS_NAMESPACE.replace('.', '_') + '*'
    EVENTS_RESOURCES = RoutingKeys.EVENTS_RESOURCES.replace('.', '_') + '*'
    EVENTS_JOB_STATUSES = RoutingKeys.EVENTS_JOB_STATUSES.replace('.', '_') + '*'
    LOGS_SIDECARS = RoutingKeys.LOGS_SIDECARS.replace('.', '_') + '*'


class CeleryTasks(object):
    """Normal celery tasks."""
    EXPERIMENTS_START = 'experiments_start'
    EXPERIMENTS_START_GROUP = 'experiments_start_group'
    CLUSTERS_UPDATE_SYSTEM_INFO = 'clusters_update_system_info'
    CLUSTERS_UPDATE_SYSTEM_NODES = 'clusters_update_system_nodes'
    CLUSTERS_UPDATE_SYSTEM_NODES_GPUS = 'clusters_update_system_nodes'


class CeleryQueues(object):
    API_EXPERIMENTS = config.get_string(
        'POLYAXON_QUEUES_API_EXPERIMENTS',
        is_optional=True) or 'api.experiments'
    API_CLUSTERS = config.get_string(
        'POLYAXON_QUEUES_API_CLUSTERS',
        is_optional=True) or 'api.clusters'
    EVENTS_NAMESPACE = config.get_string(
        'POLYAXON_QUEUES_EVENTS_NAMESPACE',
        is_optional=True) or 'events.namespace'
    EVENTS_RESOURCES = config.get_string(
        'POLYAXON_QUEUES_EVENTS_RESOURCES',
        is_optional=True) or 'events.resources'
    EVENTS_JOB_STATUSES = config.get_string(
        'POLYAXON_QUEUES_EVENTS_JOB_STATUSES',
        is_optional=True) or 'events.statuses'
    LOGS_SIDECARS = config.get_string(
        'POLYAXON_QUEUES_LOGS_SIDECARS',
        is_optional=True) or 'logs.sidecars'


class StreamQueues(object):
    # stream queues
    EVENTS_NAMESPACE = config.get_string(
        'POLYAXON_QUEUES_STREAM_EVENTS_NAMESPACE',
        is_optional=True) or 'stream.events.namespace'
    EVENTS_RESOURCES = config.get_string(
        'POLYAXON_QUEUES_STREAM_EVENTS_RESOURCES',
        is_optional=True) or 'stream.events.resources'
    EVENTS_JOB_STATUSES = config.get_string(
        'POLYAXON_QUEUES_STREAM_EVENTS_JOB_STATUSES',
        is_optional=True) or 'stream.events.jobs_statuses'
    LOGS_SIDECARS = config.get_string(
        'POLYAXON_QUEUES_STREAM_LOGS_SIDECARS',
        is_optional=True) or 'stream.logs.sidecars'


# Queues on non default exchange
CELERY_QUEUES = (
    Queue(CeleryQueues.EVENTS_NAMESPACE,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.EVENTS_NAMESPACE),
    Queue(CeleryQueues.EVENTS_RESOURCES,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.EVENTS_RESOURCES),
    Queue(CeleryQueues.EVENTS_JOB_STATUSES,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.EVENTS_JOB_STATUSES),
    Queue(CeleryQueues.LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.LOGS_SIDECARS),
)

CELERY_ROUTES = {
    CeleryTasks.EXPERIMENTS_START: {'queue': CeleryQueues.API_EXPERIMENTS},
    CeleryTasks.EXPERIMENTS_START_GROUP: {'queue': CeleryQueues.API_EXPERIMENTS},
}

CELERY_BEAT_SCHEDULE = {
    CeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO + '_BEAT': {
        'task': CeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_UPDATE_SYSTEM_INFO),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_UPDATE_SYSTEM_INFO),
            'queue': CeleryQueues.API_CLUSTERS
        },
    },
    CeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES + '_BEAT': {
        'task': CeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_UPDATE_SYSTEM_NODES),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_UPDATE_SYSTEM_NODES),
            'queue': CeleryQueues.API_CLUSTERS
        },
    },
}
