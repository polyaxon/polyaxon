from typing import Dict

from django.db import OperationalError

from db.models.nodes import ClusterEvent
from k8s_events_handlers.tasks.logger import logger
from polyaxon.celery_api import celery_app
from polyaxon.settings import K8SEventsCeleryTasks


@celery_app.task(name=K8SEventsCeleryTasks.K8S_EVENTS_HANDLE_NAMESPACE, ignore_result=True)
def k8s_handle_events_namespace(cluster_id: int, payload: Dict) -> None:
    logger.debug('handling events namespace for cluster: %s', cluster_id)
    try:
        ClusterEvent.objects.create(cluster_id=cluster_id, **payload)
    except OperationalError:
        pass
