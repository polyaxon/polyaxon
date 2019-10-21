from rest_framework import serializers

from db.models.repos import CodeReference


class CodeReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReference
        exclude = ['created_at', 'updated_at']
