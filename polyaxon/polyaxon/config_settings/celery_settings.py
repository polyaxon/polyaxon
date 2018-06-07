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


class CronsCeleryTasks(object):
    """Crons celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    EXPERIMENTS_SYNC_JOBS_STATUSES = 'experiments_sync_jobs_statuses'
    CLUSTERS_NOTIFICATION_ALIVE = 'clusters_notification_alive'
    CLUSTERS_NODES_NOTIFICATION_ALIVE = 'clusters_nodes_notification_alive'
    CLUSTERS_UPDATE_SYSTEM_NODES = 'clusters_update_system_nodes'
    CLUSTERS_UPDATE_SYSTEM_INFO = 'clusters_update_system_info'


class ReposCeleryTasks(object):
    """Pipeline celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    REPOS_HANDLE_FILE_UPLOAD = 'repos_handle_file_upload'


class PipelineCeleryTasks(object):
    """Pipeline celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    PIPELINES_START = 'pipelines_start'
    PIPELINES_START_OPERATION = 'pipelines_start_operation'
    PIPELINES_STOP_OPERATIONS = 'pipelines_stop_operations'
    PIPELINES_SKIP_OPERATIONS = 'pipelines_skip_operations'
    PIPELINES_CHECK_STATUSES = 'pipelines_check_statuses'


class CeleryOperationTasks(object):
    """Celery operation tasks.

    N.B. make sure that the task name is not < 128.
    """
    EXPERIMENTS_SCHEDULE = 'experiments_schedule'


class EventsCeleryTasks(object):
    """Runner celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    EVENTS_HANDLE_NAMESPACE = 'events_handle_namespace'
    EVENTS_HANDLE_RESOURCES = 'events_handle_resources'
    EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES = 'events_handle_experiment_job_statuses'
    EVENTS_HANDLE_JOB_STATUSES = 'events_handle_job_statuses'
    EVENTS_HANDLE_PLUGIN_JOB_STATUSES = 'events_handle_plugin_job_statuses'
    EVENTS_HANDLE_BUILD_JOB_STATUSES = 'events_handle_build_job_statuses'
    EVENTS_HANDLE_LOGS_EXPERIMENT_JOB = 'events_handle_logs_experiment_job'
    EVENTS_HANDLE_LOGS_JOB = 'events_handle_logs_job'
    EVENTS_HANDLE_LOGS_BUILD_JOB = 'events_handle_logs_build_job'


class SchedulerCeleryTasks(object):
    """Scheduler celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    EXPERIMENTS_BUILD = 'experiments_build'
    EXPERIMENTS_START = 'experiments_start'
    EXPERIMENTS_STOP = 'experiments_stop'
    EXPERIMENTS_CHECK_STATUS = 'experiments_check_status'
    EXPERIMENTS_SET_METRICS = 'experiments_set_metrics'

    EXPERIMENTS_GROUP_CREATE = 'experiments_group_create'
    EXPERIMENTS_GROUP_STOP_EXPERIMENTS = 'experiments_group_stop_experiments'
    EXPERIMENTS_GROUP_CHECK_FINISHED = 'experiments_group_check_finished'

    TENSORBOARDS_START = 'tensorboards_start'
    TENSORBOARDS_STOP = 'tensorboards_stop'

    PROJECTS_NOTEBOOK_BUILD = 'projects_notebook_build'
    PROJECTS_NOTEBOOK_START = 'projects_notebook_start'
    PROJECTS_NOTEBOOK_STOP = 'projects_notebook_stop'

    BUILD_JOBS_START = 'build_jobs_start'
    BUILD_JOBS_STOP = 'build_jobs_stop'
    BUILD_JOBS_NOTIFY_DONE = 'build_jobs_notify_done'

    JOBS_BUILD = 'jobs_build'
    JOBS_START = 'jobs_start'
    JOBS_STOP = 'jobs_stop'
    JOBS_NOTIFY_DONE = 'jobs_notify_done'


class HPCeleryTasks(object):
    """Hyperparams celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    HP_CREATE = 'hp_create'

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


class DockerizerCeleryTasks(object):
    BUILD_PROJECT_NOTEBOOK = 'build_project_notebook'
    BUILD_EXPERIMENT = 'build_experiment'


class CeleryQueues(object):
    """Celery Queues.

    N.B. make sure that the queue name is not < 128.
    """
    REPOS = config.get_string('POLYAXON_QUEUES_REPOS')

    SCHEDULER_EXPERIMENTS = config.get_string('POLYAXON_QUEUES_SCHEDULER_EXPERIMENTS')
    SCHEDULER_EXPERIMENT_GROUPS = config.get_string('POLYAXON_QUEUES_SCHEDULER_EXPERIMENT_GROUPS')
    SCHEDULER_PROJECTS = config.get_string('POLYAXON_QUEUES_SCHEDULER_PROJECTS')
    SCHEDULER_BUILD_JOBS = config.get_string('POLYAXON_QUEUES_SCHEDULER_BUILD_JOBS')

    PIPELINES = config.get_string('POLYAXON_QUEUES_PIPELINES')

    CRONS_EXPERIMENTS = config.get_string('POLYAXON_QUEUES_CRONS_EXPERIMENTS')
    CRONS_PIPELINES = config.get_string('POLYAXON_QUEUES_CRONS_PIPELINES')
    CRONS_CLUSTERS = config.get_string('POLYAXON_QUEUES_CRONS_CLUSTERS')

    HP = config.get_string('POLYAXON_QUEUES_HP')

    EVENTS_NAMESPACE = config.get_string('POLYAXON_QUEUES_EVENTS_NAMESPACE')
    EVENTS_RESOURCES = config.get_string('POLYAXON_QUEUES_EVENTS_RESOURCES')
    EVENTS_JOB_STATUSES = config.get_string('POLYAXON_QUEUES_EVENTS_JOB_STATUSES')
    LOGS_SIDECARS = config.get_string('POLYAXON_QUEUES_LOGS_SIDECARS')
    STREAM_LOGS_SIDECARS = config.get_string('POLYAXON_QUEUES_STREAM_LOGS_SIDECARS')


# Queues on non default exchange
CELERY_TASK_QUEUES = (
    Queue(CeleryQueues.STREAM_LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.LOGS_SIDECARS + '.#'),
)

CELERY_TASK_ROUTES = {
    ReposCeleryTasks.REPOS_HANDLE_FILE_UPLOAD:
        {'queue': CeleryQueues.REPOS},

    PipelineCeleryTasks.PIPELINES_START:
        {'queue': CeleryQueues.PIPELINES},
    PipelineCeleryTasks.PIPELINES_START_OPERATION:
        {'queue': CeleryQueues.PIPELINES},
    PipelineCeleryTasks.PIPELINES_STOP_OPERATIONS:
        {'queue': CeleryQueues.PIPELINES},
    PipelineCeleryTasks.PIPELINES_SKIP_OPERATIONS:
        {'queue': CeleryQueues.PIPELINES},
    PipelineCeleryTasks.PIPELINES_CHECK_STATUSES:
        {'queue': CeleryQueues.PIPELINES},
    # Operation tasks
    CeleryOperationTasks.EXPERIMENTS_SCHEDULE:
        {'queue': CeleryQueues.PIPELINES},

    CeleryPublishTask.PUBLISH_LOGS_SIDECAR:
        {'exchange': INTERNAL_EXCHANGE,
         'routing_key': RoutingKeys.LOGS_SIDECARS,
         'exchange_type': 'topic'},

    SchedulerCeleryTasks.EXPERIMENTS_START:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_STOP:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_BUILD:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_SET_METRICS:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},

    SchedulerCeleryTasks.EXPERIMENTS_GROUP_CREATE:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_CHECK_FINISHED:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},

    SchedulerCeleryTasks.TENSORBOARDS_START:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.TENSORBOARDS_STOP:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},

    SchedulerCeleryTasks.BUILD_JOBS_START:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_STOP:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_NOTIFY_DONE:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},

    SchedulerCeleryTasks.JOBS_BUILD:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.JOBS_START:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.JOBS_STOP:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.JOBS_NOTIFY_DONE:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},

    CronsCeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES:
        {'queue': CeleryQueues.CRONS_EXPERIMENTS},
    CronsCeleryTasks.CLUSTERS_NOTIFICATION_ALIVE:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE:
        {'queue': CeleryQueues.CRONS_CLUSTERS},

    HPCeleryTasks.HP_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_GRID_SEARCH_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_GRID_SEARCH_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_RANDOM_SEARCH_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_RANDOM_SEARCH_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_ITERATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_ITERATE:
        {'queue': CeleryQueues.HP},

    EventsCeleryTasks.EVENTS_HANDLE_NAMESPACE:
        {'queue': CeleryQueues.EVENTS_NAMESPACE},
    EventsCeleryTasks.EVENTS_HANDLE_RESOURCES:
        {'queue': CeleryQueues.EVENTS_RESOURCES},
    EventsCeleryTasks.EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES:
        {'queue': CeleryQueues.EVENTS_JOB_STATUSES},
    EventsCeleryTasks.EVENTS_HANDLE_JOB_STATUSES:
        {'queue': CeleryQueues.EVENTS_JOB_STATUSES},
    EventsCeleryTasks.EVENTS_HANDLE_PLUGIN_JOB_STATUSES:
        {'queue': CeleryQueues.EVENTS_JOB_STATUSES},
    EventsCeleryTasks.EVENTS_HANDLE_BUILD_JOB_STATUSES:
        {'queue': CeleryQueues.EVENTS_JOB_STATUSES},
    EventsCeleryTasks.EVENTS_HANDLE_LOGS_EXPERIMENT_JOB:
        {'queue': CeleryQueues.LOGS_SIDECARS},
    EventsCeleryTasks.EVENTS_HANDLE_LOGS_JOB:
        {'queue': CeleryQueues.LOGS_SIDECARS},
    EventsCeleryTasks.EVENTS_HANDLE_LOGS_BUILD_JOB:
        {'queue': CeleryQueues.LOGS_SIDECARS},
}

CELERY_BEAT_SCHEDULE = {
    CronsCeleryTasks.CLUSTERS_NOTIFICATION_ALIVE + '_beat': {
        'task': CronsCeleryTasks.CLUSTERS_NOTIFICATION_ALIVE,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
        },
    },
    CronsCeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES + '_beat': {
        'task': CronsCeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES,
        'schedule': Intervals.get_schedule(Intervals.EXPERIMENTS_SYNC),
        'options': {
            'expires': Intervals.get_expires(Intervals.EXPERIMENTS_SYNC),
        },
    },
    CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO + '_beat': {
        'task': CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_UPDATE_SYSTEM_INFO),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_UPDATE_SYSTEM_INFO),
        },
    },
    CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES + '_beat': {
        'task': CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_UPDATE_SYSTEM_NODES),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_UPDATE_SYSTEM_NODES),
        },
    },
    CronsCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE + '_beat': {
        'task': CronsCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE,
        'schedule': Intervals.get_schedule(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLUSTERS_NOTIFICATION_ALIVE),
        },
    },
}
