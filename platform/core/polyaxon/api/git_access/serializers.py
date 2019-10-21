from api.utils.serializers.catalog import CatalogNameSerializer, HostCatalogSerializer
from api.utils.serializers.is_default import IsDefaultSerializerMixin
from db.models.git_access import GitAccess
from options.registry.access import ACCESS_GIT


class GitAccessSerializer(HostCatalogSerializer, IsDefaultSerializerMixin):
    default_option = ACCESS_GIT
    query = GitAccess.objects

    class Meta:
        model = GitAccess
        fields = HostCatalogSerializer.Meta.fields + ('is_default', )


class GitAccessNameSerializer(CatalogNameSerializer):
    class Meta:
        model = GitAccess
        fields = CatalogNameSerializer.Meta.fields
