from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'stores.apps.StoresConfig',
    'hpsearch.apps.HPSearchConfig',
)

INSTALLED_APPS += PROJECT_APPS
