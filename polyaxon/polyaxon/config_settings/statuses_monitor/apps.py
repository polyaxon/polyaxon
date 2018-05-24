from polyaxon.config_settings.apps import *
from polyaxon.config_settings.auditor import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'statuses_monitor.apps.StatusesMonitorConfig',
)

INSTALLED_APPS += PROJECT_APPS
