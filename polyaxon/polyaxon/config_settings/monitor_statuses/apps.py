from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'monitor_statuses.apps.MonitorStatusesConfig',
)

INSTALLED_APPS += PROJECT_APPS
