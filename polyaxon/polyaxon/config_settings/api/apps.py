from ..apps import *
from ..auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'administration.apps.AdministrationConfig',
    'ownership.apps.OwnershipConfig',
    'access.apps.AccessConfig',
    'stores.apps.StoresConfig',
    'api.apps.APIsConfig',
    'publisher.apps.PublisherConfig',
    'query.apps.QueryConfig',
    'ci.apps.CIConfig',
)

INSTALLED_APPS += PROJECT_APPS
