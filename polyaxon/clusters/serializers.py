from rest_framework import fields, serializers

from models.clusters import Cluster


class ClusterSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        model = Cluster
        fields = ('uuid', 'version_api', 'created_at', 'updated_at', )
