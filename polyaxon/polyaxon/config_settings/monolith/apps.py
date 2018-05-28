from polyaxon.config_settings.apps import *
from polyaxon.config_settings.auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'api.apps.APIConfig',
    'publisher.apps.PublisherConfig',
    'scheduler.apps.SchedulerConfig',
    'hpsearch.apps.HPSearchConfig',
    'pipelines.apps.PipelinesConfig',
    'events_handlers.apps.EventsHandlersConfig',
)

INSTALLED_APPS += PROJECT_APPS
