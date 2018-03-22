from django.contrib import admin

from clusters.models import Cluster, ClusterNode, NodeGPU, ClusterEvent
from libs.admin import ReadOnlyAdmin


class ClusterEventAdmin(ReadOnlyAdmin):
    pass


admin.site.register(Cluster)
admin.site.register(ClusterNode)
admin.site.register(NodeGPU)
admin.site.register(ClusterEvent, ClusterEventAdmin)
