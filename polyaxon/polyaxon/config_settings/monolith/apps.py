from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'api.apps.APIConfig',
    'publisher.apps.PublisherConfig',
    'scheduler.apps.SchedulerConfig',
    'hpsearch.apps.HPSearchConfig',
    'pipelines.apps.PipelinesConfig',
    'events_handlers.apps.EventsHandlersConfig',
    'commands.apps.CommandsConfig',
    'rest_framework_swagger',
)

INSTALLED_APPS += PROJECT_APPS
