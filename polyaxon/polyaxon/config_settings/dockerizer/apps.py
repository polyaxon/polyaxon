from polyaxon.config_settings.auditor import AUDITOR_APPS

PROJECT_APPS = AUDITOR_APPS + (
    'publisher.apps.PublisherConfig',
    'crons.apps.CronsConfig',
)
