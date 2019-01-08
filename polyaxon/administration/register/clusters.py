from administration.register.utils import DiffModelAdmin
from db.models.clusters import Cluster


class ClusterAdmin(DiffModelAdmin):
    pass


def register(admin_register):
    admin_register(Cluster, ClusterAdmin)
