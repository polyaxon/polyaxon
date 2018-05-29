from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'monitor_resources.apps.MonitorResourcesConfig',
)

INSTALLED_APPS += PROJECT_APPS
