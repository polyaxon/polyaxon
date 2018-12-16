from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'stores.apps.StoresConfig',
    'publisher.apps.PublisherConfig',
    'scheduler.apps.SchedulerConfig',
)

INSTALLED_APPS += PROJECT_APPS
