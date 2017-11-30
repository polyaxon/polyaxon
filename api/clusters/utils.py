from django.conf import settings

from clusters.models import Cluster


def get_cluster():
    if settings.CLUSTER_ID:
        cluster = Cluster.objects.get(uuid=settings.CLUSTER_ID)
    else:
        # Get default cluster
        cluster = Cluster.objects.first()

    if cluster:
        return cluster

    cluster = Cluster.objects.create(user=settings.AUTH_USER_MODEL.objects.fist(),
                                     version_api={})
    return cluster
