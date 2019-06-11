from api.utils.serializers.catalog import CatalogSerializer
from db.models.secrets import K8SSecret


class K8SSecretSerializer(CatalogSerializer):

    class Meta:
        model = K8SSecret
        fields = CatalogSerializer.Meta.fields + (
            'keys',
            'secret_ref',
        )
