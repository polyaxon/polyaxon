from api.clusters.serializers import ClusterSerializer
from api.endpoint.base import RetrieveEndpoint
from api.endpoint.cluster import ClusterEndpoint
from db.models.clusters import Cluster


class ClusterDetailView(ClusterEndpoint, RetrieveEndpoint):
    """Get cluster details."""

    def get_serializer_class(self):
        return ClusterSerializer

    def get_object(self):
        if self._object:
            return self._object
        self._object = Cluster.load()
        return self._object
