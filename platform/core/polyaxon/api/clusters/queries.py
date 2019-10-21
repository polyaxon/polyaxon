from django.db.models import Count, Q

from db.models.clusters import Cluster

clusters = Cluster.objects.annotate(
    nodes__count=Count('nodes', filter=Q(nodes__is_current=True), distinct=True))
