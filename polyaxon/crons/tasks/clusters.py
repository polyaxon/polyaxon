import requests
import uuid

import conf

from db.models.clusters import Cluster
from polyaxon.celery_api import celery_app
from polyaxon.settings import CronsCeleryTasks


@celery_app.task(name=CronsCeleryTasks.CLUSTERS_NOTIFICATION_ALIVE,
                 time_limits=60,
                 ignore_result=True)
def cluster_analytics() -> None:
    cluster = Cluster.load()
    notification = uuid.uuid4()
    notification_url = conf.get('POLYAXON_NOTIFICATION_CLUSTER_ALIVE_URL').format(
        url=conf.get('CLUSTER_NOTIFICATION_URL'),
        cluster_uuid=cluster.uuid.hex,
        create_at=cluster.created_at.date(),
        notification=notification,
        version=conf.get('CHART_VERSION'))
    try:
        requests.get(notification_url)
    except requests.RequestException:
        pass
