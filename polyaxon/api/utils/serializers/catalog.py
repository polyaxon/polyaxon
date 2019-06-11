from rest_framework import fields, serializers


class CatalogSerializer(serializers.ModelSerializer):
    uuid = fields.UUIDField(format='hex', read_only=True)

    class Meta:
        fields = (
            'uuid',
            'name',
            'description',
            'readme',
            'tags',
            'created_at',
            'updated_at',
        )
