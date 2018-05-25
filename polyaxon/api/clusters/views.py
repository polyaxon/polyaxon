from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.nodes.serializers import ClusterRunnerSerializer
from db.models.clusters import Cluster


class ClusterDetailView(RetrieveAPIView):
    queryset = Cluster.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer_class(self):
        return ClusterRunnerSerializer

    def get_object(self):
        return Cluster.load()
