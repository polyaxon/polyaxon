from api.clusters.serializers import ClusterSerializer
from api.endpoint.base import RetrieveEndpoint
from api.endpoint.cluster import ClusterEndpoint
from db.models.clusters import Cluster


class ClusterDetailView(ClusterEndpoint, RetrieveEndpoint):
    """Get cluster details."""

    def get_serializer_class(self):
        return ClusterSerializer

    def get_object(self):
        return Cluster.load()
