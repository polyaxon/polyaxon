from administration.register.utils import ReadOnlyAdmin
from db.models.nodes import ClusterEvent, ClusterNode, NodeGPU


class ClusterEventAdmin(ReadOnlyAdmin):
    pass


def register(admin_register):
    admin_register(ClusterNode)
    admin_register(NodeGPU)
    admin_register(ClusterEvent, ClusterEventAdmin)
