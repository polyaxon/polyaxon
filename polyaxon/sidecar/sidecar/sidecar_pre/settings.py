# import os
#
# import rhea
#
# from unipath import Path
#
# def base_directory():
#     return Path(__file__).ancestor(3)
#
#
# ROOT_DIR = base_directory()
# ENV_VARS_DIR = ROOT_DIR.child('env_vars')
#
# config_values = [
#     '{}/default.json'.format(ENV_VARS_DIR),
#     os.environ,
# ]
#
# if os.path.isfile('{}/local.json'.format(ENV_VARS_DIR)):
#     config_values.append('{}/local.json'.format(ENV_VARS_DIR))
#
# config = rhea.Rhea.read_configs(config_values)
#
# K8S_NAMESPACE = config.get_string('POLYAXON_K8S_NAMESPACE')
# CONTAINER_NAME_EXPERIMENT_JOB = config.get_string('POLYAXON_CONTAINER_NAME_EXPERIMENT_JOB',
#                                                   is_optional=True,
#                                                   default='polyaxon-experiment-job')
# CONTAINER_NAME_JOB = config.get_string('POLYAXON_CONTAINER_NAME_JOB',
#                                        is_optional=True,
#                                        default='polyaxon-job')
# # Labels
# APP_LABELS_TENSORBOARD = config.get_string('POLYAXON_APP_LABELS_TENSORBOARD',
#                                            is_optional=True,
#                                            default='polyaxon-tensorboard')
# APP_LABELS_NOTEBOOK = config.get_string('POLYAXON_APP_LABELS_NOTEBOOK',
#                                         is_optional=True,
#                                         default='polyaxon-notebook')
# APP_LABELS_DOCKERIZER = config.get_string('POLYAXON_APP_LABELS_DOCKERIZER',
#                                           is_optional=True,
#                                           default='polyaxon-dockerizer')
# APP_LABELS_EXPERIMENT = config.get_string('POLYAXON_APP_LABELS_EXPERIMENT',
#                                           is_optional=True,
#                                           default='polyaxon-experiment')
# APP_LABELS_JOB = config.get_string('POLYAXON_APP_LABELS_JOB',
#                                    is_optional=True,
#                                    default='polyaxon-job')
#
# MESSAGES_COUNT = config.get_string('POLYAXON_MESSAGES_COUNT',
#                                    is_optional=True,
#                                    default=50)
# MESSAGES_TIMEOUT = config.get_string('POLYAXON_MESSAGES_TIMEOUT',
#                                      is_optional=True,
#                                      default=5)
# MESSAGES_TIMEOUT_SHORT = config.get_string('POLYAXON_MESSAGES_TIMEOUT_SHORT',
#                                            is_optional=True,
#                                            default=2)
# CHECK_ALIVE_INTERVAL = config.get_string('POLYAXON_CHECK_ALIVE_INTERVAL',
#                                          is_optional=True,
#                                          default=10)
#
# CELERY_TRACK_STARTED = True
#
# AMQP_URL = config.get_string('POLYAXON_AMQP_URL')
# RABBITMQ_USER = config.get_string('POLYAXON_RABBITMQ_USER', is_optional=True)
# RABBITMQ_PASSWORD = config.get_string('POLYAXON_RABBITMQ_PASSWORD',
#                                       is_secret=True,
#                                       is_optional=True)
# BROKER_POOL_LIMIT = None
#
# if RABBITMQ_USER and RABBITMQ_PASSWORD:
#     CELERY_BROKER_URL = 'amqp://{user}:{password}@{url}'.format(
#         user=RABBITMQ_USER,
#         password=RABBITMQ_PASSWORD,
#         url=AMQP_URL
#     )
#
# CELERY_BROKER_URL = 'amqp://{url}'.format(url=AMQP_URL)
#
# INTERNAL_EXCHANGE = config.get_string('POLYAXON_INTERNAL_EXCHANGE',
#                                       is_optional=True,
#                                       default='internal')
#
# CELERY_RESULT_BACKEND = None
# CELERYD_PREFETCH_MULTIPLIER = config.get_int('POLYAXON_CELERYD_PREFETCH_MULTIPLIER')
#
# CELERY_TASK_ALWAYS_EAGER = config.get_boolean('POLYAXON_CELERY_ALWAYS_EAGER')
# if CELERY_TASK_ALWAYS_EAGER:
#     BROKER_TRANSPORT = 'memory'
#
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_IGNORE_RESULT = True
# CELERY_IGNORE_RESULT = True
#
#
# class LogsCelerySignals(object):
#     """Logs celery signals.
#
#     N.B. make sure that the task name is not < 128.
#     """
#     LOGS_SIDECARS_EXPERIMENTS = 'logs_sidecars_experiments'
#     LOGS_SIDECARS_JOBS = 'logs_sidecars_jobs'
#     LOGS_SIDECARS_BUILDS = 'logs_sidecars_builds'
#
#
# class RoutingKeys(object):
#     LOGS_SIDECARS_EXPERIMENTS = config.get_string('POLYAXON_ROUTING_KEYS_LOGS_SIDECARS_EXPERIMENTS',
#                                                   is_optional=True,
#                                                   default='logs.sidecars.experiments')
#     LOGS_SIDECARS_JOBS = config.get_string('POLYAXON_ROUTING_KEYS_LOGS_SIDECARS_EXPERIMENTS',
#                                            is_optional=True,
#                                            default='logs.sidecars.jobs')
#     LOGS_SIDECARS_BUILDS = config.get_string('POLYAXON_ROUTING_KEYS_LOGS_SIDECARS_EXPERIMENTS',
#                                              is_optional=True,
#                                              default='logs.sidecars.builds')
#
#
# CELERY_TASK_ROUTES = {
#     LogsCelerySignals.LOGS_SIDECARS_EXPERIMENTS:
#         {'exchange': INTERNAL_EXCHANGE,
#          'routing_key': RoutingKeys.LOGS_SIDECARS_EXPERIMENTS,
#          'exchange_type': 'topic'},
#     LogsCelerySignals.LOGS_SIDECARS_JOBS:
#         {'exchange': INTERNAL_EXCHANGE,
#          'routing_key': RoutingKeys.LOGS_SIDECARS_JOBS,
#          'exchange_type': 'topic'},
#     LogsCelerySignals.LOGS_SIDECARS_BUILDS:
#         {'exchange': INTERNAL_EXCHANGE,
#          'routing_key': RoutingKeys.LOGS_SIDECARS_BUILDS,
#          'exchange_type': 'topic'}
# }
