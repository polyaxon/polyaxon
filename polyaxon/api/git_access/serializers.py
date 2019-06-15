from api.utils.serializers.catalog import CatalogNameSerializer, HostCatalogSerializer
from db.models.git_access import GitAccess


class GitAccessSerializer(HostCatalogSerializer):
    QUERY = GitAccess.objects

    class Meta:
        model = GitAccess
        fields = HostCatalogSerializer.Meta.fields


class GitAccessNameSerializer(CatalogNameSerializer):
    class Meta:
        model = GitAccess
        fields = CatalogNameSerializer.Meta.fields
