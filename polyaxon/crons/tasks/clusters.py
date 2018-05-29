import requests
import uuid

from django.conf import settings

from db.models.clusters import Cluster
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CronsCeleryTasks


@celery_app.task(name=CronsCeleryTasks.CLUSTERS_NOTIFICATION_ALIVE,
                 time_limits=60,
                 ignore_result=True)
def cluster_analytics():
    cluster = Cluster.load()
    notification = uuid.uuid4()
    notification_url = settings.POLYAXON_NOTIFICATION_CLUSTER_ALIVE_URL.format(
        url=settings.CLUSTER_NOTIFICATION_URL,
        cluster_uuid=cluster.uuid.hex,
        create_at=cluster.created_at.date(),
        notification=notification,
        version=settings.CHART_VERSION)
    try:
        requests.get(notification_url)
    except requests.RequestException:
        pass
