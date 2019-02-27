from datetime import timedelta

from kombu import Exchange, Queue

from polyaxon.config_manager import config

CELERY_TRACK_STARTED = True

AMQP_URL = config.get_string('POLYAXON_AMQP_URL')
RABBITMQ_USER = config.get_string('POLYAXON_RABBITMQ_USER', is_optional=True)
RABBITMQ_PASSWORD = config.get_string('POLYAXON_RABBITMQ_PASSWORD',
                                      is_secret=True,
                                      is_optional=True)
BROKER_POOL_LIMIT = None

if RABBITMQ_USER and RABBITMQ_PASSWORD:
    CELERY_BROKER_URL = 'amqp://{user}:{password}@{url}'.format(
        user=RABBITMQ_USER,
        password=RABBITMQ_PASSWORD,
        url=AMQP_URL
    )

# todo: fix me at some point
CELERY_BROKER_URL = 'amqp://{url}'.format(url=AMQP_URL)

INTERNAL_EXCHANGE = config.get_string('POLYAXON_INTERNAL_EXCHANGE',
                                      is_optional=True,
                                      default='internal')

CELERY_RESULT_BACKEND = config.get_string('POLYAXON_REDIS_CELERY_RESULT_BACKEND_URL')
CELERYD_PREFETCH_MULTIPLIER = config.get_int('POLYAXON_CELERYD_PREFETCH_MULTIPLIER')

CELERY_TASK_ALWAYS_EAGER = config.get_boolean('POLYAXON_CELERY_ALWAYS_EAGER')
if CELERY_TASK_ALWAYS_EAGER:
    BROKER_TRANSPORT = 'memory'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_IGNORE_RESULT = True
CELERY_IGNORE_RESULT = True
CELERY_HARD_TIME_LIMIT_DELAY = config.get_int('POLYAXON_CELERY_HARD_TIME_LIMIT_DELAY',
                                              is_optional=True,
                                              default=180)
HEALTH_CHECK_WORKER_TIMEOUT = config.get_int('POLYAXON_HEALTH_CHECK_WORKER_TIMEOUT',
                                             is_optional=True,
                                             default=4)
CELERYD_MAX_TASKS_PER_CHILD = config.get_int('POLYAXON_CELERYD_MAX_TASKS_PER_CHILD',
                                             is_optional=True,
                                             default=100)
GROUP_CHUNKS = config.get_int('POLYAXON_GROUP_CHUNKS',
                              is_optional=True,
                              default=50)


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
    HEARTBEAT_CHECK = config.get_int(
        'POLYAXON_INTERVALS_HEARTBEAT_CHECK',
        is_optional=True,
        default=60 * 10)
    CLUSTERS_NOTIFICATION_ALIVE = 150
    CLEAN_ACTIVITY_LOGS = config.get_int(
        'POLYAXON_INTERVALS_CLEAN_ACTIVITY_LOGS',
        is_optional=True,
        default=300)
    CLEAN_NOTIFICATIONS = config.get_int(
        'POLYAXON_INTERVALS_CLEAN_NOTIFICATIONS',
        is_optional=True,
        default=300)
    DELETE_ARCHIVED = config.get_int(
        'POLYAXON_INTERVALS_DELETE_ARCHIVED',
        is_optional=True,
        default=300)

    @staticmethod
    def get_schedule(interval):
        return timedelta(seconds=int(interval))

    @staticmethod
    def get_expires(interval):
        int(interval / 2)


class RoutingKeys(object):
    STREAM_LOGS_SIDECARS_EXPERIMENTS = config.get_string(
        'POLYAXON_ROUTING_KEYS_STREAM_LOGS_SIDECARS_EXPERIMENTS',
        is_optional=True,
        default='stream_logs.sidecars.experiments')
    STREAM_LOGS_SIDECARS_JOBS = config.get_string(
        'POLYAXON_ROUTING_KEYS_STREAM_LOGS_SIDECARS_JOBS',
        is_optional=True,
        default='stream_logs.sidecars.jobs')
    STREAM_LOGS_SIDECARS_BUILDS = config.get_string(
        'POLYAXON_ROUTING_KEYS_STREAM_LOGS_SIDECARS_BUILDS',
        is_optional=True,
        default='stream_logs.sidecars.builds')

    LOGS_SIDECARS = config.get_string(
        'POLYAXON_ROUTING_KEYS_LOGS_SIDECARS',
        is_optional=True,
        default='logs.sidecars.*')


class CeleryPublishTask(object):
    """Tasks to be send as a signal to the exchange."""
    PUBLISH_LOGS_SIDECAR_EXPERIMENTS = 'publish_logs_sidecar_experiments'
    PUBLISH_LOGS_SIDECAR_JOBS = 'publish_logs_sidecar_jobs'
    PUBLISH_LOGS_SIDECAR_BUILDS = 'publish_logs_sidecar_builds'


class CronsCeleryTasks(object):
    """Crons celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    CRONS_HEALTH = 'crons_health'

    EXPERIMENTS_SYNC_JOBS_STATUSES = 'experiments_sync_jobs_statuses'

    HEARTBEAT_EXPERIMENTS = 'heartbeat_experiments'
    HEARTBEAT_JOBS = 'heartbeat_jobs'
    HEARTBEAT_BUILDS = 'heartbeat_builds'

    CLUSTERS_NOTIFICATION_ALIVE = 'clusters_notification_alive'
    CLUSTERS_NODES_NOTIFICATION_ALIVE = 'clusters_nodes_notification_alive'
    CLUSTERS_UPDATE_SYSTEM_NODES = 'clusters_update_system_nodes'
    CLUSTERS_UPDATE_SYSTEM_INFO = 'clusters_update_system_info'
    CLEAN_ACTIVITY_LOGS = 'clean_activity_logs'
    CLEAN_NOTIFICATIONS = 'clean_notifications'

    DELETE_ARCHIVED_PROJECTS = 'delete_archived_projects'
    DELETE_ARCHIVED_EXPERIMENT_GROUPS = 'delete_archived_experiment_groups'
    DELETE_ARCHIVED_EXPERIMENTS = 'delete_archived_experiments'
    DELETE_ARCHIVED_JOBS = 'delete_archived_jobs'
    DELETE_ARCHIVED_BUILD_JOBS = 'delete_archived_build_jobs'
    DELETE_ARCHIVED_NOTEBOOK_JOBS = 'delete_archived_notebook_jobs'
    DELETE_ARCHIVED_TENSORBOARD_JOBS = 'delete_archived_tensorboard_jobs'


class ReposCeleryTasks(object):
    """Pipeline celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    REPOS_HANDLE_FILE_UPLOAD = 'repos_handle_file_upload'


class PipelinesCeleryTasks(object):
    """Pipeline celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    PIPELINES_HEALTH = 'pipelines_health'
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


class K8SEventsCeleryTasks(object):
    """Runner celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    K8S_EVENTS_HEALTH = 'k8s_events_health'
    K8S_EVENTS_HANDLE_NAMESPACE = 'k8s_events_handle_namespace'
    K8S_EVENTS_HANDLE_RESOURCES = 'k8s_events_handle_resources'
    K8S_EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES = 'k8s_events_handle_experiment_job_statuses'
    K8S_EVENTS_HANDLE_JOB_STATUSES = 'k8s_events_handle_job_statuses'
    K8S_EVENTS_HANDLE_PLUGIN_JOB_STATUSES = 'k8s_events_handle_plugin_job_statuses'
    K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES = 'k8s_events_handle_build_job_statuses'


class EventsCeleryTasks(object):
    """Runner celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    EVENTS_HEALTH = 'events_health'
    EVENTS_NOTIFY = 'events_notify'
    EVENTS_TRACK = 'events_track'
    EVENTS_LOG = 'events_log'


class LogsCeleryTasks(object):
    """Logs celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    LOGS_HEALTH = 'logs_health'
    LOGS_HANDLE_EXPERIMENT_JOB = 'logs_handle_experiment_job'
    LOGS_HANDLE_JOB = 'logs_handle_job'
    LOGS_HANDLE_BUILD_JOB = 'logs_handle_build_job'

    # Signals
    LOGS_SIDECARS_EXPERIMENTS = 'logs_sidecars_experiments'
    LOGS_SIDECARS_JOBS = 'logs_sidecars_jobs'
    LOGS_SIDECARS_BUILDS = 'logs_sidecars_builds'


class SchedulerCeleryTasks(object):
    """Scheduler celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    SCHEDULER_HEALTH = 'scheduler_health'

    EXPERIMENTS_BUILD = 'experiments_build'
    EXPERIMENTS_START = 'experiments_start'
    EXPERIMENTS_STOP = 'experiments_stop'
    EXPERIMENTS_CHECK_STATUS = 'experiments_check_status'
    EXPERIMENTS_CHECK_HEARTBEAT = 'experiments_check_heartbeat'
    EXPERIMENTS_SET_METRICS = 'experiments_set_metrics'
    EXPERIMENTS_SCHEDULE_DELETION = 'experiments_schedule_deletion'

    EXPERIMENTS_GROUP_CREATE = 'experiments_group_create'
    EXPERIMENTS_GROUP_STOP = 'experiments_group_stop'
    EXPERIMENTS_GROUP_STOP_EXPERIMENTS = 'experiments_group_stop_experiments'
    EXPERIMENTS_GROUP_CHECK_FINISHED = 'experiments_group_check_finished'
    EXPERIMENTS_GROUP_SCHEDULE_DELETION = 'experiments_group_schedule_deletion'

    TENSORBOARDS_START = 'tensorboards_start'
    TENSORBOARDS_STOP = 'tensorboards_stop'
    TENSORBOARDS_SCHEDULE_DELETION = 'tensorboards_schedule_deletion'

    PROJECTS_NOTEBOOK_BUILD = 'projects_notebook_build'
    PROJECTS_NOTEBOOK_START = 'projects_notebook_start'
    PROJECTS_NOTEBOOK_STOP = 'projects_notebook_stop'
    PROJECTS_NOTEBOOK_SCHEDULE_DELETION = 'projects_notebook_schedule_deletion'

    BUILD_JOBS_START = 'build_jobs_start'
    BUILD_JOBS_STOP = 'build_jobs_stop'
    BUILD_JOBS_NOTIFY_DONE = 'build_jobs_notify_done'
    BUILD_JOBS_SET_DOCKERFILE = 'build_jobs_set_dockerfile'
    BUILD_JOBS_CHECK_HEARTBEAT = 'build_jobs_check_heartbeat'
    BUILD_JOBS_SCHEDULE_DELETION = 'build_jobs_schedule_deletion'

    JOBS_BUILD = 'jobs_build'
    JOBS_START = 'jobs_start'
    JOBS_STOP = 'jobs_stop'
    JOBS_NOTIFY_DONE = 'jobs_notify_done'
    JOBS_CHECK_HEARTBEAT = 'jobs_check_heartbeat'
    JOBS_SCHEDULE_DELETION = 'jobs_schedule_deletion'

    PROJECTS_SCHEDULE_DELETION = 'projects_schedule_deletion'

    STORES_SCHEDULE_DATA_DELETION = 'stores_schedule_data_deletion'
    STORES_SCHEDULE_OUTPUTS_DELETION = 'stores_schedule_outputs_deletion'
    STORES_SCHEDULE_LOGS_DELETION = 'stores_schedule_logs_deletion'

    DELETE_ARCHIVED_PROJECT = 'delete_archived_project'
    DELETE_ARCHIVED_EXPERIMENT_GROUP = 'delete_archived_experiment_group'
    DELETE_ARCHIVED_EXPERIMENT = 'delete_archived_experiment'
    DELETE_ARCHIVED_JOB = 'delete_archived_job'
    DELETE_ARCHIVED_BUILD_JOB = 'delete_archived_build_job'
    DELETE_ARCHIVED_NOTEBOOK_JOB = 'delete_archived_notebook_job'
    DELETE_ARCHIVED_TENSORBOARD_JOB = 'delete_archived_tensorboard_job'


class HPCeleryTasks(object):
    """Hyperparams celery tasks.

    N.B. make sure that the task name is not < 128.
    """
    HP_HEALTH = 'hp_health'

    HP_CREATE = 'hp_create'
    HP_START = 'hp_start'

    HP_GRID_SEARCH_CREATE = 'hp_grid_search_create'
    HP_GRID_SEARCH_CREATE_EXPERIMENTS = 'hp_grid_search_create_experiments'
    HP_GRID_SEARCH_START = 'hp_grid_search_start'

    HP_RANDOM_SEARCH_CREATE = 'hp_random_search_create'
    HP_RANDOM_SEARCH_CREATE_EXPERIMENTS = 'hp_random_search_create_experiments'
    HP_RANDOM_SEARCH_START = 'hp_random_search_start'

    HP_HYPERBAND_CREATE = 'hp_hyperband_create'
    HP_HYPERBAND_CREATE_EXPERIMENTS = 'hp_hyperband_create_experiments'
    HP_HYPERBAND_START = 'hp_hyperband_start'
    HP_HYPERBAND_ITERATE = 'hp_hyperband_iterate'

    HP_BO_CREATE = 'hp_bo_create'
    HP_BO_CREATE_EXPERIMENTS = 'hp_bo_create_experiments'
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

    SCHEDULER_HEALTH = config.get_string('POLYAXON_QUEUES_SCHEDULER_HEALTH')
    SCHEDULER_EXPERIMENTS = config.get_string('POLYAXON_QUEUES_SCHEDULER_EXPERIMENTS')
    SCHEDULER_EXPERIMENT_GROUPS = config.get_string('POLYAXON_QUEUES_SCHEDULER_EXPERIMENT_GROUPS')
    SCHEDULER_PROJECTS = config.get_string('POLYAXON_QUEUES_SCHEDULER_PROJECTS')
    SCHEDULER_STORES = config.get_string('POLYAXON_QUEUES_SCHEDULER_STORES')
    SCHEDULER_BUILD_JOBS = config.get_string('POLYAXON_QUEUES_SCHEDULER_BUILD_JOBS')
    SCHEDULER_JOBS = config.get_string('POLYAXON_QUEUES_SCHEDULER_JOBS')
    SCHEDULER_CLEAN = config.get_string('POLYAXON_QUEUES_SCHEDULER_CLEAN')

    PIPELINES_HEALTH = config.get_string('POLYAXON_QUEUES_PIPELINES_HEALTH')
    PIPELINES = config.get_string('POLYAXON_QUEUES_PIPELINES')

    CRONS_HEALTH = config.get_string('POLYAXON_QUEUES_CRONS_HEALTH')
    CRONS_HEARTBEAT = config.get_string('POLYAXON_QUEUES_CRONS_HEARTBEAT')
    CRONS_EXPERIMENTS = config.get_string('POLYAXON_QUEUES_CRONS_EXPERIMENTS')
    CRONS_PIPELINES = config.get_string('POLYAXON_QUEUES_CRONS_PIPELINES')
    CRONS_CLUSTERS = config.get_string('POLYAXON_QUEUES_CRONS_CLUSTERS')
    CRONS_CLEAN = config.get_string('POLYAXON_QUEUES_CRONS_CLEAN')

    HP_HEALTH = config.get_string('POLYAXON_QUEUES_HP_HEALTH')
    HP = config.get_string('POLYAXON_QUEUES_HP')

    EVENTS_HEALTH = config.get_string('POLYAXON_QUEUES_EVENTS_HEALTH')
    EVENTS_NOTIFY = config.get_string('POLYAXON_QUEUES_EVENTS_NOTIFY')
    EVENTS_LOG = config.get_string('POLYAXON_QUEUES_EVENTS_LOG')
    EVENTS_TRACK = config.get_string('POLYAXON_QUEUES_EVENTS_TRACK')

    K8S_EVENTS_HEALTH = config.get_string('POLYAXON_QUEUES_K8S_EVENTS_HEALTH')
    K8S_EVENTS_NAMESPACE = config.get_string('POLYAXON_QUEUES_K8S_EVENTS_NAMESPACE')
    K8S_EVENTS_RESOURCES = config.get_string('POLYAXON_QUEUES_K8S_EVENTS_RESOURCES')
    K8S_EVENTS_JOB_STATUSES = config.get_string('POLYAXON_QUEUES_K8S_EVENTS_JOB_STATUSES')

    LOGS_HEALTH = config.get_string('POLYAXON_QUEUES_LOGS_HEALTH')
    LOGS_SIDECARS = config.get_string('POLYAXON_QUEUES_LOGS_SIDECARS')
    LOGS_HANDLERS = config.get_string('POLYAXON_QUEUES_LOGS_HANDLERS')
    STREAM_LOGS_SIDECARS = config.get_string('POLYAXON_QUEUES_STREAM_LOGS_SIDECARS')


# Queues on non default exchange
CELERY_TASK_QUEUES = (
    # Streams
    Queue(CeleryQueues.STREAM_LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.STREAM_LOGS_SIDECARS_EXPERIMENTS + '.#'),
    Queue(CeleryQueues.STREAM_LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.STREAM_LOGS_SIDECARS_JOBS + '.#'),
    Queue(CeleryQueues.STREAM_LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.STREAM_LOGS_SIDECARS_BUILDS + '.#'),

    # Sidecars signals
    Queue(CeleryQueues.LOGS_SIDECARS,
          exchange=Exchange(INTERNAL_EXCHANGE, 'topic'),
          routing_key=RoutingKeys.LOGS_SIDECARS),
)

CELERY_TASK_ROUTES = {
    ReposCeleryTasks.REPOS_HANDLE_FILE_UPLOAD:
        {'queue': CeleryQueues.REPOS},

    # Pipelines and ops Health
    PipelinesCeleryTasks.PIPELINES_HEALTH:
        {'queue': CeleryQueues.PIPELINES_HEALTH},
    # Pipelines tasks
    PipelinesCeleryTasks.PIPELINES_START:
        {'queue': CeleryQueues.PIPELINES},
    PipelinesCeleryTasks.PIPELINES_START_OPERATION:
        {'queue': CeleryQueues.PIPELINES},
    PipelinesCeleryTasks.PIPELINES_STOP_OPERATIONS:
        {'queue': CeleryQueues.PIPELINES},
    PipelinesCeleryTasks.PIPELINES_SKIP_OPERATIONS:
        {'queue': CeleryQueues.PIPELINES},
    PipelinesCeleryTasks.PIPELINES_CHECK_STATUSES:
        {'queue': CeleryQueues.PIPELINES},
    # Operation tasks
    CeleryOperationTasks.EXPERIMENTS_SCHEDULE:
        {'queue': CeleryQueues.PIPELINES},

    CeleryPublishTask.PUBLISH_LOGS_SIDECAR_EXPERIMENTS:
        {'exchange': INTERNAL_EXCHANGE,
         'routing_key': RoutingKeys.STREAM_LOGS_SIDECARS_EXPERIMENTS,
         'exchange_type': 'topic'},
    CeleryPublishTask.PUBLISH_LOGS_SIDECAR_JOBS:
        {'exchange': INTERNAL_EXCHANGE,
         'routing_key': RoutingKeys.STREAM_LOGS_SIDECARS_JOBS,
         'exchange_type': 'topic'},
    CeleryPublishTask.PUBLISH_LOGS_SIDECAR_BUILDS:
        {'exchange': INTERNAL_EXCHANGE,
         'routing_key': RoutingKeys.STREAM_LOGS_SIDECARS_BUILDS,
         'exchange_type': 'topic'},

    # Scheduler health
    SchedulerCeleryTasks.SCHEDULER_HEALTH:
        {'queue': CeleryQueues.SCHEDULER_HEALTH},

    # Scheduler experiments
    SchedulerCeleryTasks.EXPERIMENTS_START:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_STOP:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_BUILD:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_CHECK_STATUS:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_CHECK_HEARTBEAT:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_SET_METRICS:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},
    SchedulerCeleryTasks.EXPERIMENTS_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENTS},

    # Scheduler groups
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_CREATE:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_STOP_EXPERIMENTS:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_CHECK_FINISHED:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},
    SchedulerCeleryTasks.EXPERIMENTS_GROUP_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},

    # Scheduler tensorboards/notebooks
    SchedulerCeleryTasks.TENSORBOARDS_START:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.TENSORBOARDS_STOP:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.TENSORBOARDS_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_BUILD:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_START:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},
    SchedulerCeleryTasks.PROJECTS_NOTEBOOK_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},

    # Scheduler builds
    SchedulerCeleryTasks.BUILD_JOBS_START:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_STOP:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_NOTIFY_DONE:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_SET_DOCKERFILE:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_CHECK_HEARTBEAT:
        {'queue': CeleryQueues.SCHEDULER_BUILD_JOBS},
    SchedulerCeleryTasks.BUILD_JOBS_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},

    # Scheduler jobs
    SchedulerCeleryTasks.JOBS_BUILD:
        {'queue': CeleryQueues.SCHEDULER_JOBS},
    SchedulerCeleryTasks.JOBS_START:
        {'queue': CeleryQueues.SCHEDULER_JOBS},
    SchedulerCeleryTasks.JOBS_STOP:
        {'queue': CeleryQueues.SCHEDULER_JOBS},
    SchedulerCeleryTasks.JOBS_NOTIFY_DONE:
        {'queue': CeleryQueues.SCHEDULER_JOBS},
    SchedulerCeleryTasks.JOBS_CHECK_HEARTBEAT:
        {'queue': CeleryQueues.SCHEDULER_JOBS},
    SchedulerCeleryTasks.JOBS_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_EXPERIMENT_GROUPS},

    # Scheduler projects
    SchedulerCeleryTasks.PROJECTS_SCHEDULE_DELETION:
        {'queue': CeleryQueues.SCHEDULER_PROJECTS},

    # Scheduler stores
    SchedulerCeleryTasks.STORES_SCHEDULE_DATA_DELETION:
        {'queue': CeleryQueues.SCHEDULER_STORES},
    SchedulerCeleryTasks.STORES_SCHEDULE_OUTPUTS_DELETION:
        {'queue': CeleryQueues.SCHEDULER_STORES},
    SchedulerCeleryTasks.STORES_SCHEDULE_LOGS_DELETION:
        {'queue': CeleryQueues.SCHEDULER_STORES},

    # Scheduler deletion
    SchedulerCeleryTasks.DELETE_ARCHIVED_PROJECT:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},
    SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUP:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},
    SchedulerCeleryTasks.DELETE_ARCHIVED_EXPERIMENT:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},
    SchedulerCeleryTasks.DELETE_ARCHIVED_JOB:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},
    SchedulerCeleryTasks.DELETE_ARCHIVED_BUILD_JOB:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},
    SchedulerCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOB:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},
    SchedulerCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOB:
        {'queue': CeleryQueues.SCHEDULER_CLEAN},


    # Crons health
    CronsCeleryTasks.CRONS_HEALTH:
        {'queue': CeleryQueues.CRONS_HEALTH},

    # Crons
    CronsCeleryTasks.EXPERIMENTS_SYNC_JOBS_STATUSES:
        {'queue': CeleryQueues.CRONS_EXPERIMENTS},

    CronsCeleryTasks.HEARTBEAT_EXPERIMENTS:
        {'queue': CeleryQueues.CRONS_HEARTBEAT},
    CronsCeleryTasks.HEARTBEAT_JOBS:
        {'queue': CeleryQueues.CRONS_HEARTBEAT},
    CronsCeleryTasks.HEARTBEAT_BUILDS:
        {'queue': CeleryQueues.CRONS_HEARTBEAT},

    CronsCeleryTasks.CLUSTERS_NOTIFICATION_ALIVE:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLUSTERS_NODES_NOTIFICATION_ALIVE:
        {'queue': CeleryQueues.CRONS_CLUSTERS},
    CronsCeleryTasks.CLEAN_ACTIVITY_LOGS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.CLEAN_NOTIFICATIONS:
        {'queue': CeleryQueues.CRONS_CLEAN},

    CronsCeleryTasks.DELETE_ARCHIVED_PROJECTS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUPS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENTS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.DELETE_ARCHIVED_JOBS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOBS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOBS:
        {'queue': CeleryQueues.CRONS_CLEAN},
    CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOBS:
        {'queue': CeleryQueues.CRONS_CLEAN},

    # HP health
    HPCeleryTasks.HP_HEALTH:
        {'queue': CeleryQueues.HP_HEALTH},
    # HP ops
    HPCeleryTasks.HP_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_GRID_SEARCH_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_GRID_SEARCH_CREATE_EXPERIMENTS:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_GRID_SEARCH_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_RANDOM_SEARCH_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_RANDOM_SEARCH_CREATE_EXPERIMENTS:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_RANDOM_SEARCH_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_CREATE_EXPERIMENTS:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_HYPERBAND_ITERATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_CREATE:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_CREATE_EXPERIMENTS:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_START:
        {'queue': CeleryQueues.HP},
    HPCeleryTasks.HP_BO_ITERATE:
        {'queue': CeleryQueues.HP},

    # Events health
    EventsCeleryTasks.EVENTS_HEALTH:
        {'queue': CeleryQueues.EVENTS_HEALTH},

    # Events ops
    EventsCeleryTasks.EVENTS_NOTIFY:
        {'queue': CeleryQueues.EVENTS_NOTIFY},
    EventsCeleryTasks.EVENTS_TRACK:
        {'queue': CeleryQueues.EVENTS_TRACK},
    EventsCeleryTasks.EVENTS_LOG:
        {'queue': CeleryQueues.EVENTS_LOG},

    # K8S Events health
    K8SEventsCeleryTasks.K8S_EVENTS_HEALTH:
        {'queue': CeleryQueues.K8S_EVENTS_HEALTH},

    # K8S Events ops
    K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_NAMESPACE:
        {'queue': CeleryQueues.K8S_EVENTS_NAMESPACE},
    K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_RESOURCES:
        {'queue': CeleryQueues.K8S_EVENTS_RESOURCES},
    K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_EXPERIMENT_JOB_STATUSES:
        {'queue': CeleryQueues.K8S_EVENTS_JOB_STATUSES},
    K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_JOB_STATUSES:
        {'queue': CeleryQueues.K8S_EVENTS_JOB_STATUSES},
    K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_PLUGIN_JOB_STATUSES:
        {'queue': CeleryQueues.K8S_EVENTS_JOB_STATUSES},
    K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_BUILD_JOB_STATUSES:
        {'queue': CeleryQueues.K8S_EVENTS_JOB_STATUSES},

    # Logs health
    LogsCeleryTasks.LOGS_HEALTH:
        {'queue': CeleryQueues.LOGS_HEALTH},

    # Logs ops
    LogsCeleryTasks.LOGS_HANDLE_EXPERIMENT_JOB:
        {'queue': CeleryQueues.LOGS_HANDLERS},
    LogsCeleryTasks.LOGS_HANDLE_JOB:
        {'queue': CeleryQueues.LOGS_HANDLERS},
    LogsCeleryTasks.LOGS_HANDLE_BUILD_JOB:
        {'queue': CeleryQueues.LOGS_HANDLERS},
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
    CronsCeleryTasks.HEARTBEAT_EXPERIMENTS + '_beat': {
        'task': CronsCeleryTasks.HEARTBEAT_EXPERIMENTS,
        'schedule': Intervals.get_schedule(Intervals.HEARTBEAT_CHECK),
        'options': {
            'expires': Intervals.get_expires(Intervals.HEARTBEAT_CHECK),
        },
    },
    CronsCeleryTasks.HEARTBEAT_JOBS + '_beat': {
        'task': CronsCeleryTasks.HEARTBEAT_JOBS,
        'schedule': Intervals.get_schedule(Intervals.HEARTBEAT_CHECK),
        'options': {
            'expires': Intervals.get_expires(Intervals.HEARTBEAT_CHECK),
        },
    },
    CronsCeleryTasks.HEARTBEAT_BUILDS + '_beat': {
        'task': CronsCeleryTasks.HEARTBEAT_BUILDS,
        'schedule': Intervals.get_schedule(Intervals.HEARTBEAT_CHECK),
        'options': {
            'expires': Intervals.get_expires(Intervals.HEARTBEAT_CHECK),
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
    CronsCeleryTasks.CLEAN_ACTIVITY_LOGS + '_beat': {
        'task': CronsCeleryTasks.CLEAN_ACTIVITY_LOGS,
        'schedule': Intervals.get_schedule(Intervals.CLEAN_ACTIVITY_LOGS),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLEAN_ACTIVITY_LOGS),
        },
    },
    CronsCeleryTasks.CLEAN_NOTIFICATIONS + '_beat': {
        'task': CronsCeleryTasks.CLEAN_NOTIFICATIONS,
        'schedule': Intervals.get_schedule(Intervals.CLEAN_NOTIFICATIONS),
        'options': {
            'expires': Intervals.get_expires(Intervals.CLEAN_NOTIFICATIONS),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_PROJECTS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_PROJECTS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUPS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENT_GROUPS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENTS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_EXPERIMENTS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_JOBS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_JOBS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOBS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_BUILD_JOBS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOBS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_NOTEBOOK_JOBS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
    CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOBS + '_beat': {
        'task': CronsCeleryTasks.DELETE_ARCHIVED_TENSORBOARD_JOBS,
        'schedule': Intervals.get_schedule(Intervals.DELETE_ARCHIVED),
        'options': {
            'expires': Intervals.get_expires(Intervals.DELETE_ARCHIVED),
        },
    },
}
