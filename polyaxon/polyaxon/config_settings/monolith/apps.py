from ..auditor_apps import AUDITOR_APPS
from ..debug import *

PROJECT_APPS = AUDITOR_APPS + (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'administration.apps.AdministrationConfig',
    'ownership.apps.OwnershipConfig',
    'access.apps.AccessConfig',
    'stores.apps.StoresConfig',
    'compiler.apps.CompilerConfig',
    'api.apps.APIConfig',
    'query.apps.QueryConfig',
    'publisher.apps.PublisherConfig',
    'scheduler.apps.SchedulerConfig',
    'hpsearch.apps.HPSearchConfig',
    'events_handlers.apps.EventsHandlersConfig',
    'k8s_events_handlers.apps.K8SEventsHandlersConfig',
    'commands.apps.CommandsConfig',
    'ci.apps.CIConfig',
)

INSTALLED_APPS += PROJECT_APPS
