from rest_framework import fields, serializers

from api.nodes.serializers import ClusterNodeSerializer
from db.models.clusters import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    nodes = ClusterNodeSerializer(many=True)

    class Meta:
        model = Cluster
        fields = ('uuid', 'version_api', 'created_at', 'updated_at', 'nodes', )
