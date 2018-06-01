from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'hpsearch.apps.HPSearchConfig',
)

INSTALLED_APPS += PROJECT_APPS
