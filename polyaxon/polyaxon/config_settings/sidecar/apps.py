from polyaxon.config_settings.apps import *

PROJECT_APPS = (
    'publisher.apps.PublisherConfig',
    'sidecar.apps.SideCarConfig',
)

INSTALLED_APPS += PROJECT_APPS
