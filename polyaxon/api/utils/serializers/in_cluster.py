from rest_framework import serializers


class InClusterMixin(serializers.Serializer):
    in_cluster = serializers.NullBooleanField(initial=True, default=True)

    def validate_in_cluster(self, value):
        return value if isinstance(value, bool) else True
