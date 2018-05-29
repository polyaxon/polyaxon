from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'resources_monitor.apps.ResourcesMonitorConfig',
)

INSTALLED_APPS += PROJECT_APPS
