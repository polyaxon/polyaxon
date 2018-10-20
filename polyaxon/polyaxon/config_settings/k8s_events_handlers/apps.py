from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'publisher.apps.PublisherConfig',
    'k8s_events_handlers.apps.K8SEventsHandlersConfig',
)

INSTALLED_APPS += PROJECT_APPS
