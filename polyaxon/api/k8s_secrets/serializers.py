from api.utils.serializers.catalog import K8SResourceCatalogSerializer
from db.models.secrets import K8SSecret


class K8SSecretSerializer(K8SResourceCatalogSerializer):
    class Meta:
        model = K8SSecret
        fields = K8SResourceCatalogSerializer.Meta.fields
