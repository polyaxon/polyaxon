from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.conf import settings

from db.models.clusters import Cluster
from apis.clusters.serializers import ClusterSerializer


class ClusterDetailView(RetrieveAPIView):
    queryset = Cluster.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_serializer_class(self):
        if settings.DEPLOY_RUNNER:
            from apis.nodes import ClusterRunnerSerializer
            return ClusterRunnerSerializer
        return ClusterSerializer

    def get_object(self):
        return Cluster.load()
