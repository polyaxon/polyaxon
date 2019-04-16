from polyaxon.config_manager import config

DEFAULT_APPS = (
    'polyaxon',
    'conf.apps.ConfConfig',
    'db.apps.DBConfig',
)

EXTRA_APPS = config.get_string('POLYAXON_EXTRA_APPS', is_list=True, is_optional=True)
EXTRA_APPS = tuple(EXTRA_APPS) if EXTRA_APPS else ()

THIRD_PARTY_APPS = (
    'rest_framework',
    'corsheaders',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
)

INSTALLED_APPS += THIRD_PARTY_APPS + DEFAULT_APPS + EXTRA_APPS
