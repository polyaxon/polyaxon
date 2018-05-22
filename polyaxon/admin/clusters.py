from django.contrib import admin

from models.clusters import Cluster
from libs.admin import DiffModelAdmin


class ClusterAdmin(DiffModelAdmin):
    pass


admin.site.register(Cluster, ClusterAdmin)
