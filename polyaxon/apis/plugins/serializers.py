from rest_framework import fields, serializers

from libs.spec_validation import validate_plugin_spec_config
from db.models.plugins import NotebookJob, TensorboardJob


class PluginJobBaseSerializer(serializers.ModelSerializer):
    user = fields.SerializerMethodField()

    class Meta:
        fields = ('user', 'config',)

    def get_user(self, obj):
        return obj.user.username

    def _validate_spec(self, values):
        # content is optional
        if not values:
            return values

        validate_plugin_spec_config(values)

        # Resume normal creation
        return values

    def validate_config(self, config):
        return self._validate_spec(config)


class TensorboardJobSerializer(PluginJobBaseSerializer):
    class Meta(PluginJobBaseSerializer.Meta):
        model = TensorboardJob


class NotebookJobSerializer(PluginJobBaseSerializer):
    class Meta(PluginJobBaseSerializer.Meta):
        model = NotebookJob
