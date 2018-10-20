from ..auditor_apps import AUDITOR_APPS
from ..debug import *

PROJECT_APPS = AUDITOR_APPS + (
    'api.apps.APIConfig',
    'publisher.apps.PublisherConfig',
    'scheduler.apps.SchedulerConfig',
    'hpsearch.apps.HPSearchConfig',
    'pipelines.apps.PipelinesConfig',
    'events_handlers.apps.EventsHandlersConfig',
    'k8s_events_handlers.apps.K8SEventsHandlersConfig',
    'logs_handlers.apps.LogsHandlersConfig',
    'commands.apps.CommandsConfig',
)

INSTALLED_APPS += PROJECT_APPS
