from polyaxon.config_settings.apps import *
from polyaxon.config_settings.auditor_apps import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'suggester.apps.SuggesterConfig',
)

INSTALLED_APPS += PROJECT_APPS
