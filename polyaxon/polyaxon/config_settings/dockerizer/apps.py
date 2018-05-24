from polyaxon.config_settings.apps import *

PROJECT_APPS = (
    'publisher.apps.PublisherConfig',
    'dockerizer.apps.DockerizerConfig',
)

INSTALLED_APPS += PROJECT_APPS
