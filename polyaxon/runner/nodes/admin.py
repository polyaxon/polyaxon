from django.contrib import admin

from libs.admin import ReadOnlyAdmin
from runner.nodes.models import ClusterEvent, ClusterNode, NodeGPU


class ClusterEventAdmin(ReadOnlyAdmin):
    pass


admin.site.register(ClusterNode)
admin.site.register(NodeGPU)
admin.site.register(ClusterEvent, ClusterEventAdmin)
