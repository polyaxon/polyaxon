import os

from celery import Celery

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    del os.environ['DJANGO_SETTINGS_MODULE']

app = Celery('polyaxon-sidecar')
app.config_from_object('sidecar.settings', namespace='CELERY')
celery_app = app
