from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'api.apps.APIsConfig',
)

INSTALLED_APPS += PROJECT_APPS
