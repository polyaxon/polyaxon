from api.utils.serializers.catalog import CatalogSerializer
from db.models.config_maps import K8SConfigMap


class K8SConfigMapSerializer(CatalogSerializer):

    class Meta:
        model = K8SConfigMap
        fields = CatalogSerializer.Meta.fields + (
            'keys',
            'config_map_ref',
        )
