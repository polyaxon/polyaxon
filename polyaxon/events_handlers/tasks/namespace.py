from django.db import OperationalError

from db.models.nodes import ClusterEvent
from events_handlers.tasks.logger import logger
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import EventsCeleryTasks


@celery_app.task(name=EventsCeleryTasks.EVENTS_HANDLE_NAMESPACE, ignore_result=True)
def handle_events_namespace(cluster_id, payload):
    logger.debug('handling events namespace for cluster: %s', cluster_id)
    try:
        ClusterEvent.objects.create(cluster_id=cluster_id, **payload)
    except OperationalError:
        pass
