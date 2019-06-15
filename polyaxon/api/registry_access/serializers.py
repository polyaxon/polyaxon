from api.utils.serializers.catalog import CatalogNameSerializer, HostCatalogSerializer
from api.utils.serializers.is_default import IsDefaultSerializerMixin
from db.models.registry_access import RegistryAccess
from options.registry.access import ACCESS_REGISTRY


class RegistryAccessSerializer(HostCatalogSerializer, IsDefaultSerializerMixin):
    default_option = ACCESS_REGISTRY
    query = RegistryAccess.objects

    class Meta:
        model = RegistryAccess
        fields = HostCatalogSerializer.Meta.fields + ('is_default', )


class RegistryAccessNameSerializer(CatalogNameSerializer):
    class Meta:
        model = RegistryAccess
        fields = CatalogNameSerializer.Meta.fields
