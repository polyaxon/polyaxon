from rest_framework import fields, serializers


class CatalogSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        fields = (
            'id',
            'uuid',
            'name',
            'description',
            'readme',
            'tags',
            'created_at',
            'updated_at',
        )


class K8SResourceCatalogSerializer(CatalogSerializer):
    class Meta:
        fields = CatalogSerializer.Meta.fields + (
            'k8s_ref',
            'keys',
        )
