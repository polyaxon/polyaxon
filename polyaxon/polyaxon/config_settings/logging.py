import os

from polyaxon.config_manager import ROOT_DIR, config

LOG_DIRECTORY = ROOT_DIR.child('logs')
if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(message)s [%(name)s:%(lineno)s]',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)8s  %(message)s [%(name)s]'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'logfile': {
            'level': config.log_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/polyaxon_{}.log'.format(LOG_DIRECTORY, os.getpid()),
            'maxBytes': 1024 * 1024 * 8,  # 8 MByte
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': config.log_level,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'celery': {
            'handlers': config.log_handlers,
            'level': config.log_level
        },
        'polyaxon.streams': {
            'propagate': True,
            'handlers': config.log_handlers,
            'level': config.log_level,
        },
        'polyaxon.monitors': {
            'propagate': True,
            'handlers': config.log_handlers,
            'level': config.log_level,
        },
        'polyaxon.dockerizer': {
            'propagate': True,
            'handlers': config.log_handlers,
            'level': config.log_level,
        },
        'django.request': {
            'propagate': True,
            'handlers': config.log_handlers,
            'level': config.log_level,
        },
        'root': {
            'handlers': config.log_handlers,
            'level': config.log_level,
        },
        'sanic.error': {
            'propagate': True,
            'handlers': config.log_handlers,
            'level': config.log_level,
            'qualname': 'sanic.error'
        },

        'sanic.access': {
            'propagate': True,
            'handlers': config.log_handlers,
            'level': config.log_level,
            'qualname': 'sanic.access'
        }
    },
}

RAVEN_CONFIG = {}
if not (config.is_testing_env or config.is_local_env) and config.platform_dsn:
    RAVEN_CONFIG['dsn'] = config.platform_dsn
    RAVEN_CONFIG['transport'] = 'raven.transport.threaded_requests.ThreadedRequestsHTTPTransport'
    RAVEN_CONFIG['release'] = config.get_string('POLYAXON_CHART_VERSION',
                                                is_optional=True,
                                                default='0.0.0')
    RAVEN_CONFIG['IGNORE_EXCEPTIONS'] = config.ignore_exceptions + [
        'django.db.ProgrammingError',
        'django.db.OperationalError',
        'django.db.InterfaceError'
    ]
    RAVEN_CONFIG['environment'] = config.env
