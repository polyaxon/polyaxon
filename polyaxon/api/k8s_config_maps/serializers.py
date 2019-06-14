from api.utils.serializers.catalog import K8SResourceCatalogSerializer
from db.models.config_maps import K8SConfigMap


class K8SConfigMapSerializer(K8SResourceCatalogSerializer):
    QUERY = K8SConfigMap.objects

    class Meta:
        model = K8SConfigMap
        fields = K8SResourceCatalogSerializer.Meta.fields
