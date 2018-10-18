from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'publisher.apps.PublisherConfig',
    'logs_handlers.apps.LogsHandlersConfig',
)

INSTALLED_APPS += PROJECT_APPS
