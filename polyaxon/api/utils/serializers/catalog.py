from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.names import CatalogNamesMixin
from api.utils.serializers.tags import TagsSerializerMixin


class CatalogSerializer(serializers.ModelSerializer, CatalogNamesMixin, TagsSerializerMixin):
    query = None

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

    def update(self, instance, validated_data):
        validated_data = self.validated_tags(validated_data=validated_data,
                                             tags=instance.tags)
        validated_data = self.validated_name(validated_data,
                                             owner=instance.owner,
                                             query=self.query)

        return super().update(instance=instance, validated_data=validated_data)

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             owner=validated_data['owner'],
                                             query=self.query)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)


class CatalogNameSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name',)


class K8SResourceCatalogSerializer(CatalogSerializer):
    class Meta:
        fields = CatalogSerializer.Meta.fields + (
            'k8s_ref',
            'items',
        )


class AccessCatalogSerializer(CatalogSerializer):
    class Meta:
        fields = CatalogSerializer.Meta.fields + (
            'k8s_secret',
        )


class HostCatalogSerializer(AccessCatalogSerializer):
    host = fields.CharField(required=False)

    class Meta:
        fields = AccessCatalogSerializer.Meta.fields + (
            'host',
        )
