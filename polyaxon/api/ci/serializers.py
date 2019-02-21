from rest_framework import serializers

from db.models.ci import CI


class CISerializer(serializers.ModelSerializer):

    class Meta:
        model = CI
        fields = ('config', 'created_at', 'updated_at',)
