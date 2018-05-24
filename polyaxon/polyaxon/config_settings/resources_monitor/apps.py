from polyaxon.config_settings.apps import *
from polyaxon.config_settings.auditor import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'resources_monitor.apps.ResourcesMonitorConfig',
)

INSTALLED_APPS += PROJECT_APPS
