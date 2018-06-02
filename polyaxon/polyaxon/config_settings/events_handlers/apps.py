from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'publisher.apps.PublisherConfig',
    'events_handlers.apps.EventsHandlersConfig',
)

INSTALLED_APPS += PROJECT_APPS
