from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'stores.apps.StoresConfig',
    'ownership.apps.OwnershipConfig',
    'commands.apps.CommandsConfig',
    'publisher.apps.PublisherConfig',
)

INSTALLED_APPS += PROJECT_APPS
