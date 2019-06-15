from api.utils.serializers.catalog import CatalogNameSerializer, K8SResourceCatalogSerializer
from db.models.secrets import K8SSecret


class K8SSecretSerializer(K8SResourceCatalogSerializer):
    query = K8SSecret.objects

    class Meta:
        model = K8SSecret
        fields = K8SResourceCatalogSerializer.Meta.fields


class K8SSecretNameSerializer(CatalogNameSerializer):
    class Meta:
        model = K8SSecret
        fields = CatalogNameSerializer.Meta.fields
