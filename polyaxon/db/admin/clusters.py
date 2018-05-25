from django.contrib import admin

from db.admin.utils import DiffModelAdmin
from db.models.clusters import Cluster


class ClusterAdmin(DiffModelAdmin):
    pass


admin.site.register(Cluster, ClusterAdmin)
