from rest_framework import serializers, fields

from db.models.config_options import ConfigOption


class ConfigOptionSerializer(serializers.ModelSerializer):
    option = fields.SerializerMethodField()

    class Meta:
        model = ConfigOption
        fields = (
            'key',
            'option',
            'is_secret',
        )

    def get_option(self, obj):
        return obj.secret if obj.is_secret else obj.value
