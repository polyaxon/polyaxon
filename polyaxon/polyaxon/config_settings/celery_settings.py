from datetime import timedelta

from kombu import Exchange, Queue

from polyaxon.utils import config

CELERY_TRACK_STARTED = True

AMQP_URL = config.get_string('POLYAXON_AMQP_URL')
RABBITMQ_USER = config.get_string(
    'POLYAXON_RABBITMQ_USER', is_optional=True)
RABBITMQ_PASSWORD = config.get_string(
    'POLYAXON_RABBITMQ_PASSWORD', is_secret=True, is_optional=True)
if RABBITMQ_USER and RABBITMQ_PASSWORD:
    CELERY_BROKER_URL = 'amqp://{user}:{password}@{url}'.format(
        user=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
        url=AMQP_URL
    )

CELERY_BROKER_URL = 'amqp://{url}'.format(url=AMQP_URL)

INTERNAL_EXCHANGE = config.get_string('POLYAXON_INTERNAL_EXCHANGE')

# CELERY_RESULT_BACKEND = config.get_string('POLYAXON_REDIS_CELERY_RESULT_BACKEND_URL')
CELERYD_PREFETCH_MULTIPLIER = config.get_int('POLYAXON_CELERYD_PREFETCH_MULTIPLIER')

CELERY_TASK_ALWAYS_EAGER = config.get_boolean('POLYAXON_CELERY_ALWAYS_EAGER')
if CELERY_TASK_ALWAYS_EAGER:
    BROKER_TRANSPORT = 'memory'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_IGNORE_RESULT = True
CELERY_HARD_TIME_LIMIT_DELAY = config.get_int('POLYAXON_CELERY_HARD_TIME_LIMIT_DELAY',
                                              is_optional=True,
                                              default=180)


class Intervals(object):
    """All intervals are in seconds"""
    OPERATIONS_DEFAULT_RETRY_DELAY = config.get_int(
        'POLYAXON_INTERVALS_OPERATIONS_DEFAULT_RETRY_DELAY',
        is_optional=True,
        default=60)
    OPERATIONS_MAX_RETRY_DELAY = config.get_int(
        'POLYAXON_INTERVALS_OPERATIONS_MAX_RETRY_DELAY',
        is_optional=True,
        default=60 * 60)
    PIPELINES_SCHEDULER = config.get_int(
        'POLYAXON_INTERVALS_PIPELINES_SCHEDULER',
        is_optional=True,
        default=30)
    EXPERIMENTS_SCHEDULER = config.get_int(
        'POLYAXON_INTERVALS_EXPERIMENTS_SCHEDULER',
        is_optional=True,
        default=30)
    EXPERIMENTS_SYNC = config.get_int(
        'POLYAXON_INTERVALS_EXPERIMENTS_SYNC',
        is_optional=True,
        default=30)
    CLUSTERS_UPDATE_SYSTEM_INFO = config.get_int(
        'POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_INFO',
        is_optional=True,
        default=150)
    CLUSTERS_UPDATE_SYSTEM_NODES = config.get_int(
        'POLYAXON_INTERVALS_CLUSTERS_UPDATE_SYSTEM_NODES',
        is_optional=True,
        default=150)
    CLUSTERS_NOTIFICATION_ALIVE = 150

    @staticmethod
    def get_schedule(interval):
        return timedelta(seconds=int(interval))

    @staticmethod
    def get_expires(interval):
        int(interval / 2)


class RoutingKeys(object):
    LOGS_SIDECARS = config.get_string('POLYAXON_ROUTING_KEYS_LOGS_SIDECARS')


class CeleryPublishTask(object):
    """Tasks to be send as a signal to the exchange."""
    PUBLISH_LOGS_SIDECAR = 'publish_logs_sidecar'


class CeleryTasks(object):
    """Normal celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    EXPERIMENTS_CHECK_STATUS = 'experiments_check_status'
    EXPERIMENTS_SET_METRICS = 'experiments_set_metrics'
    EXPERIMENTS_SYNC_JOBS_STATUSES = 'experiments_sync_jobs_statuses'

    REPOS_HANDLE_FILE_UPLOAD = 'repos_handle_file_upload'

    CLUSTERS_NOTIFICATION_ALIVE = 'clusters_notification_alive'

    PIPELINES_START = 'pipelines_start'
    PIPELINES_START_OPERATION = 'pipelines_start_operation'
    PIPELINES_STOP_OPERATIONS = 'pipelines_stop_operations'
    PIPELINES_SKIP_OPERATIONS = 'pipelines_skip_operations'
    PIPELINES_CHECK_STATUSES = 'pipelines_check_statuses'


class RunnerCeleryTasks(object):
    """Runner celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    CLUSTERS_NODES_NOTIFICATION_ALIVE = 'clusters_nodes_notification_alive'
    CLUSTERS_UPDATE_SYSTEM_NODES = 'clusters_update_system_nodes'
    CLUSTERS_UPDATE_SYSTEM_INFO = 'clusters_update_system_info'

    EXPERIMENTS_BUILD = 'experiments_build'
    EXPERIMENTS_START = 'experiments_start'
    EXPERIMENTS_STOP = 'experiments_stop'

    EXPERIMENTS_GROUP_CREATE = 'experiments_group_create'
    EXPERIMENTS_GROUP_STOP_EXPERIMENTS = 'experiments_group_stop_experiments'
    EXPERIMENTS_GROUP_CHECK_FINISHED = 'experiments_group_check_finished'

    PROJECTS_TENSORBOARD_START = 'projects_tensorboard_start'
    PROJECTS_TENSORBOARD_STOP = 'projects_tensorboard_stop'
    PROJECTS_NOTEBOOK_BUILD = 'projects_notebook_build'
    PROJECTS_NOTEBOOK_START = 'projects_notebook_start'
    PROJECTS_NOTEBOOK_STOP = 'projects_notebook_stop'

    EVENTS_HANDLE_NAMESPACE = 'events_handle_namespace'
    EVENTS_HANDLE_RESOURCES = 'events_handle_resources'
    EVENTS_HANDLE_JOB_STATUSES = 'events_handle_job_statuses'
    EVENTS_HANDLE_PLUGIN_JOB_STATUSES = 'events_handle_plugin_job_statuses'
    EVENTS_HANDLE_LOGS_SIDECAR = 'events_handle_logs_sidecar'


class HPCeleryTasks(object):
    """Hyperparams celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    HP_GRID_SEARCH_CREATE = 'hp_grid_search_create'
    HP_GRID_SEARCH_START = 'hp_grid_search_start'

    HP_RANDOM_SEARCH_CREATE = 'hp_random_search_create'
    HP_RANDOM_SEARCH_START = 'hp_random_search_start'

    HP_HYPERBAND_CREATE = 'hp_hyperband_create'
    HP_HYPERBAND_START = 'hp_hyperband_start'
    HP_HYPERBAND_ITERATE = 'hp_hyperband_iterate'

    HP_BO_CREATE = 'hp_bo_create'
    HP_BO_START = 'hp_bo_start'
    HP_BO_ITERATE = 'hp_bo_iterate'


class CeleryOperationTasks(object):
    """Celery operation tasks.

    N.B. make sure that the task name is not < 128.
    """
    EXPERIMENTS_SCHEDULE = 'experiments_schedule'


class CeleryQueues(object):
    """Celery Queues.

    N.B. make sure that the queue name is not < 128.
    """
    API_EXPERIMENTS = config.get_string(
        'POLYAXON_QUEUES_API_EXPERIMENTS',
        is_optional=True,
        default='api.experiments')
    API_EXPERIMENTS_SYNC = config.get_string(
        'POLYAXON_QUEUES_API_EXPERIMENTS_SYNC',
        is_optional=True,
        default='api.sync_experiments')
    API_CLUSTERS = config.get_string(
        'POLYAXON_QUEUES_API_CLUSTERS',
        is_optional=True,
        default='api.commands')
    API_PIPELINES = config.get_string(
        'POLYAXON_QUEUES_API_PIPELINES',
        is_optional=True,
        default='api.pipelines')
    EVENTS_NAMESPACE = config.get_string(
        'POLYAXON_QUEUES_EVENTS_NAMESPACE',
        is_optional=True,
        default='events.namespace')
    EVENTS_RESOURCES = config.get_string(
        'POLYAXON_QUEUES_EVENTS_RESOURCES',
        is_optional=True,
        default='events.resources')
    EVENTS_JOB_STATUSES = config.get_string(
        'POLYAXON_QUEUES_EVENTS_JOB_STATUSES',
        is_optional=True,
        default='events.constants')
    LOGS_SIDECARS = config.get_string(
        'POLYAXON_QUEUES_LOGS_SIDECARS',
        is_optional=True,
        default='logs.sidecars')
    STREAM_LOGS_SIDECARS = config.get_string(
        'POLYAXON_QUEUES_STREAM_LOGS_SIDECARS',
        is_optional=True,
        default='stream.logs.sidecars')


# Queues on non default exchange
CELERY_TASK_QUEUES = (
    Queue(CeleryQueues.STREAM_LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.LOGS_SIDECARS + '.#'),
)

CELERY_TASK_ROUTES = {
    CeleryTasks.EXPERIMENTS_CHECK_STATUS: {'queue': CeleryQueues.API_EXPERIMENTS},
    CeleryTasks.REPOS_HANDLE_FILE_UPLOAD: {'queue': CeleryQueues.API_EXPERIMENTS},
    CeleryTasks.EXPERIMENTS_SET_METRICS: {'queue': CeleryQueues.API_EXPERIMENTS},
    CeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES: {'queue': CeleryQueues.API_EXPERIMENTS_SYNC},
    CeleryTasks.CLUSTERS_NOTIFICATION_ALIVE: {'queue': CeleryQueues.API_CLUSTERS},

    # Pipelines
    CeleryTasks.PIPELINES_START: {'queue': CeleryQueues.API_PIPELINES},
    CeleryTasks.PIPELINES_START_OPERATION: {'queue': CeleryQueues.API_PIPELINES},
    CeleryTasks.PIPELINES_STOP_OPERATIONS: {'queue': CeleryQueues.API_PIPELINES},
    CeleryTasks.PIPELINES_SKIP_OPERATIONS: {'queue': CeleryQueues.API_PIPELINES},
    CeleryTasks.PIPELINES_CHECK_STATUSES: {'queue': CeleryQueues.API_PIPELINES},

    # Operation tasks
    CeleryOperationTasks.EXPERIMENTS_SCHEDULE: {'queue': CeleryQueues.API_PIPELINES},

    CeleryPublishTask.PUBLISH_LOGS_SIDECAR: {'exchange': INTERNAL_EXCHANGE,
                                             'routing_key': RoutingKeys.LOGS_SIDECARS,
                                             'exchange_type': 'topic'},
}

CELERY_BEAT_SCHEDULE = {
    CeleryTasks.CLUSTERS_NOTIFICATION_ALIVE + '_beat': {
        'task': CeleryTasks.CLUSTERS_NOTIFICATION_ALIVE,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
        },
    },
    CeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES + '_beat': {
        'task': CeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES,
        'schedule': Intervals.get_schedule(Intervals.EXPERIMENTS_SYNC),
        'options': {
            'expires': Intervals.get_expires(Intervals.EXPERIMENTS_SYNC),
        },
    },
}

if config.get_boolean('POLYAXON_DEPLOY_RUNNER', is_optional=True, default=True):
    CELERY_TASK_ROUTES.update({
        RunnerCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO: {'queue': CeleryQueues.API_CLUSTERS},
        RunnerCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES: {'queue': CeleryQueues.API_CLUSTERS},
        RunnerCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE: {'queue': CeleryQueues.API_CLUSTERS},

        RunnerCeleryTasks.EXPERIMENTS_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.EXPERIMENTS_STOP: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.EXPERIMENTS_BUILD: {'queue': CeleryQueues.API_EXPERIMENTS},

        RunnerCeleryTasks.EXPERIMENTS_GROUP_CREATE: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS:
            {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.EXPERIMENTS_GROUP_CHECK_FINISHED:
            {'queue': CeleryQueues.API_EXPERIMENTS},

        HPCeleryTasks.HP_GRID_SEARCH_CREATE: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_GRID_SEARCH_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_RANDOM_SEARCH_CREATE: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_RANDOM_SEARCH_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_HYPERBAND_CREATE: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_HYPERBAND_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_HYPERBAND_ITERATE: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_BO_CREATE: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_BO_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        HPCeleryTasks.HP_BO_ITERATE: {'queue': CeleryQueues.API_EXPERIMENTS},

        RunnerCeleryTasks.PROJECTS_TENSORBOARD_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.PROJECTS_TENSORBOARD_STOP: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.PROJECTS_NOTEBOOK_BUILD: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.PROJECTS_NOTEBOOK_START: {'queue': CeleryQueues.API_EXPERIMENTS},
        RunnerCeleryTasks.PROJECTS_NOTEBOOK_STOP: {'queue': CeleryQueues.API_EXPERIMENTS},

        # Monitors
        RunnerCeleryTasks.EVENTS_HANDLE_NAMESPACE: {'queue': CeleryQueues.EVENTS_NAMESPACE},
        RunnerCeleryTasks.EVENTS_HANDLE_RESOURCES: {'queue': CeleryQueues.EVENTS_RESOURCES},
        RunnerCeleryTasks.EVENTS_HANDLE_JOB_STATUSES: {'queue': CeleryQueues.EVENTS_JOB_STATUSES},
        RunnerCeleryTasks.EVENTS_HANDLE_PLUGIN_JOB_STATUSES:
            {'queue': CeleryQueues.EVENTS_JOB_STATUSES},
        RunnerCeleryTasks.EVENTS_HANDLE_LOGS_SIDECAR: {'queue': CeleryQueues.LOGS_SIDECARS},
    })

    CELERY_BEAT_SCHEDULE.update({
        RunnerCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO + '_beat': {
            'task': RunnerCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO,
            'schedule': Intervals.get_schedule(Intervals.CLUSTERS_UPDATE_SYSTEM_INFO),
            'options': {
                'expires': Intervals.get_expires(Intervals.CLUSTERS_UPDATE_SYSTEM_INFO),
            },
        },
        RunnerCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES + '_beat': {
            'task': RunnerCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES,
            'schedule': Intervals.get_schedule(Intervals.CLUSTERS_UPDATE_SYSTEM_NODES),
            'options': {
                'expires': Intervals.get_expires(Intervals.CLUSTERS_UPDATE_SYSTEM_NODES),
            },
        },
        RunnerCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE + '_beat': {
            'task': RunnerCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE,
            'schedule': Intervals.get_schedule(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
            'options': {
                'expires': Intervals.get_expires(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
            },
        },
    })
