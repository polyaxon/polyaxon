from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'monitor_statuses.apps.StatusesMonitorConfig',
)

INSTALLED_APPS += THIRD_PARTY_APPS + PROJECT_APPS
