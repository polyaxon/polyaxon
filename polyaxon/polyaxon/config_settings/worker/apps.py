from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'stores.apps.StoresConfig',
    'compiler.apps.CompilerConfig',
    'publisher.apps.PublisherConfig',
    'scheduler.apps.SchedulerConfig',
    'events_handlers.apps.EventsHandlersConfig',
    'ci.apps.CIConfig',
    'crons.apps.CronsConfig',
)

INSTALLED_APPS += PROJECT_APPS
