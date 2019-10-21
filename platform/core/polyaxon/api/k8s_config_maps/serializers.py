from api.utils.serializers.catalog import CatalogNameSerializer, K8SResourceCatalogSerializer
from db.models.config_maps import K8SConfigMap


class K8SConfigMapSerializer(K8SResourceCatalogSerializer):
    query = K8SConfigMap.objects

    class Meta:
        model = K8SConfigMap
        fields = K8SResourceCatalogSerializer.Meta.fields


class K8SConfigMapNameSerializer(CatalogNameSerializer):
    class Meta:
        model = K8SConfigMap
        fields = CatalogNameSerializer.Meta.fields
