from django.contrib import admin

from db.models.clusters import Cluster
from db.admin.utils import DiffModelAdmin


class ClusterAdmin(DiffModelAdmin):
    pass


admin.site.register(Cluster, ClusterAdmin)
