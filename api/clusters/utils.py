from django.conf import settings

from clusters.models import Cluster


def get_cluster():
    if settings.CLUSTER_ID:
        return Cluster.objects.get(uuid=settings.CLUSTER_ID)
    else:
        # Get default cluster
        return Cluster.objects.first()
