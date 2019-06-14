from api.utils.serializers.catalog import CatalogSerializer
from db.models.data_stores import DataStore


class DataStoreSerializer(CatalogSerializer):
    QUERY = DataStore.objects

    class Meta:
        model = DataStore
        fields = CatalogSerializer.Meta.fields + (
            'type',
            'mount_path',
            'host_path',
            'volume_claim',
            'bucket',
            'k8s_secret',
            'read_only'
        )
