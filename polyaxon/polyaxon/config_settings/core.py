from polyaxon.config_manager import config

DEBUG = config.is_debug_mode
POLYAXON_SERVICE = config.service
POLYAXON_ENVIRONMENT = config.env
K8S_NAMESPACE = config.namespace
K8S_NODE_NAME = config.node_name
K8S_GPU_RESOURCE_KEY = config.get_string('POLYAXON_K8S_GPU_RESOURCE_KEY')
K8S_TPU_RESOURCE_KEY = config.get_string('POLYAXON_K8S_TPU_RESOURCE_KEY',
                                         is_optional=True,
                                         default='cloud-tpus.google.com/v2')
CONF_BACKEND = config.get_string('POLYAXON_CONF_BACKEND', is_optional=True)
CLUSTER_ID = config.cluster_id
REPOS_ARCHIVE_ROOT = '/tmp/archived_repos'
OUTPUTS_ARCHIVE_ROOT = '/tmp/archived_outputs'
OUTPUTS_DOWNLOAD_ROOT = '/tmp/download_outputs'
LOGS_DOWNLOAD_ROOT = '/tmp/download_logs'
LOGS_ARCHIVE_ROOT = '/tmp/archived_logs'
FILE_UPLOAD_PERMISSIONS = 0o644
ADMIN_VIEW_ENABLED = config.get_boolean('POLYAXON_ADMIN_VIEW_ENABLED',
                                        is_optional=True,
                                        default=False)
# Global Async Countdown
GLOBAL_COUNTDOWN = config.get_int('POLYAXON_GLOBAL_COUNTDOWN',
                                  is_optional=True,
                                  default=1)
# Heartbeat timeout (status -> failed as zombie)
TTL_HEARTBEAT = config.get_int('POLYAXON_TTL_HEARTBEAT',
                               is_optional=True,
                               default=60 * 30)
# Token time in days
TTL_TOKEN = config.get_int('POLYAXON_TTL_TOKEN',
                           is_optional=True,
                           default=30)
# Ephemeral token ttl
TTL_EPHEMERAL_TOKEN = config.get_int('POLYAXON_TTL_EPHEMERAL_TOKEN',
                                     is_optional=True,
                                     default=60 * 60 * 3)

# Group checks interval
GROUP_CHECKS_INTERVAL = config.get_int('POLYAXON_GROUP_CHECKS_INTERVAL',
                                       is_optional=True,
                                       default=5)

# Auditor backend
AUDITOR_BACKEND = config.get_string('POLYAXON_AUDITOR_BACKEND', is_optional=True)


def get_allowed_hosts():
    allowed_hosts = config.get_string('POLYAXON_ALLOWED_HOSTS',
                                      is_optional=True,
                                      is_list=True,
                                      default=['*'])
    allowed_hosts.append('.polyaxon.com')
    k8s_api_host = config.get_string('POLYAXON_K8S_API_HOST', is_optional=True)
    if k8s_api_host:
        allowed_hosts.append(k8s_api_host)

    return allowed_hosts


ALLOWED_HOSTS = get_allowed_hosts()

WSGI_APPLICATION = 'polyaxon.wsgi.application'
TIME_ZONE = config.get_string('POLYAXON_TIME_ZONE', is_optional=True) or 'Europe/Berlin'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', u'English'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

INTERNAL_IPS = ('127.0.0.1',)
APPEND_SLASH = True

ROOT_URLCONF = 'polyaxon.urls'
AUTH_USER_MODEL = 'db.User'

# user management
LOGIN_URL = '/users/login/'
LOGOUT_REDIRECT_URL = LOGIN_URL
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7
INVITATION_TIMEOUT_DAYS = 30

SESSION_COOKIE_AGE = 24 * 60 * 60  # 24 hours
SESSION_COOKIE_HTTPONLY = True

DEFAULT_DB_ENGINE = 'django.db.backends.postgresql'
DATABASES = {
    'default': {
        'ENGINE': config.get_string('POLYAXON_DB_ENGINE', is_optional=True) or DEFAULT_DB_ENGINE,
        'NAME': config.get_string('POLYAXON_DB_NAME'),
        'USER': config.get_string('POLYAXON_DB_USER'),
        'PASSWORD': config.get_string('POLYAXON_DB_PASSWORD', is_secret=True),
        'HOST': config.get_string('POLYAXON_DB_HOST'),
        'PORT': config.get_string('POLYAXON_DB_PORT'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': config.get_int('POLYAXON_DB_CONN_MAX_AGE', is_optional=True, default=0),
    }
}
