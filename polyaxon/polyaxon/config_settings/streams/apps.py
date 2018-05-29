from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'statuses_monitor.apps.StatusesMonitorConfig',
)

INSTALLED_APPS += THIRD_PARTY_APPS + PROJECT_APPS
