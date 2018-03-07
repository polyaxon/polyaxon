# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.contrib import admin

from clusters.models import Cluster, ClusterNode, NodeGPU, ClusterEvent
from libs.admin import ReadOnlyAdmin


class ClusterEventAdmin(ReadOnlyAdmin):
    pass


admin.site.register(Cluster)
admin.site.register(ClusterNode)
admin.site.register(NodeGPU)
admin.site.register(ClusterEvent, ClusterEventAdmin)
