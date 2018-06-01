from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'streams.apps.StreamsConfig',
)

INSTALLED_APPS += PROJECT_APPS
