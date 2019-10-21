from api.utils.serializers.catalog import AccessCatalogSerializer, CatalogNameSerializer
from db.models.data_stores import DataStore


class DataStoreSerializer(AccessCatalogSerializer):
    query = DataStore.objects

    class Meta:
        model = DataStore
        fields = AccessCatalogSerializer.Meta.fields + (
            'type',
            'mount_path',
            'host_path',
            'volume_claim',
            'bucket',
            'read_only'
        )


class DataStoreNameSerializer(CatalogNameSerializer):
    class Meta:
        model = DataStore
        fields = CatalogNameSerializer.Meta.fields
