import os

from polyaxon.utils import ROOT_DIR, config

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
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/polyaxon_{}.log'.format(LOG_DIRECTORY, os.getpid()),
            'maxBytes': 1024 * 1024 * 8,  # 8 MByte
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'polyaxon.streams': {
            'handlers': ['console', ],
            'propagate': True,
            'level': 'INFO',
        },
        'polyaxon.monitors': {
            'handlers': ['console', ],
            'propagate': True,
            'level': 'INFO',
        },
        'polyaxon.dockerizer': {
            'handlers': ['console', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console', ],
        },
    },
}

RAVEN_CONFIG = {}
if not (config.is_testing_env or config.is_local_env):
    RAVEN_CONFIG['dsn'] = config.platform_dns
    RAVEN_CONFIG['transport'] = "raven.transport.threaded_requests.ThreadedRequestsHTTPTransport"
    RAVEN_CONFIG['release'] = config.get_string('POLYAXON_CHART_VERSION',
                                                is_optional=True,
                                                default='0.0.0')
    RAVEN_CONFIG['environment'] = config.env
