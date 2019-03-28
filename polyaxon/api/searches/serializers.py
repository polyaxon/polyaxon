from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.utils.serializers.names import NamesMixin
from db.models.searches import Search


class SearchSerializer(serializers.ModelSerializer, NamesMixin):
    class Meta:
        model = Search
        fields = ['id', 'name', 'query', 'meta']

    def create(self, validated_data):
        validated_data = self.validated_name(validated_data,
                                             project=validated_data['project'],
                                             query=Search.objects)
        try:
            return super().create(validated_data)
        except Exception as e:
            raise ValidationError(e)
