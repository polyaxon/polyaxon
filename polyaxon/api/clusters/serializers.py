from rest_framework import fields, serializers
from rest_framework.fields import SerializerMethodField

from api.nodes.serializers import ClusterNodeSerializer
from db.models.clusters import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)
    nodes = SerializerMethodField()

    def get_nodes(self, cluster: 'Cluster'):
        qs = cluster.nodes.filter(is_current=True)
        serializer = ClusterNodeSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Cluster
        fields = ('uuid', 'version_api', 'created_at', 'updated_at', 'nodes', )
