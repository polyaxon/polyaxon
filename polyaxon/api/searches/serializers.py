from rest_framework import serializers

from db.models.searches import Search


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = ['id', 'name', 'query', 'meta']
