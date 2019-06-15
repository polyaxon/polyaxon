from api.utils.serializers.catalog import CatalogNameSerializer, HostCatalogSerializer
from db.models.registry_access import RegistryAccess


class RegistryAccessSerializer(HostCatalogSerializer):
    QUERY = RegistryAccess.objects

    class Meta:
        model = RegistryAccess
        fields = HostCatalogSerializer.Meta.fields


class RegistryAccessNameSerializer(CatalogNameSerializer):
    class Meta:
        model = RegistryAccess
        fields = CatalogNameSerializer.Meta.fields
