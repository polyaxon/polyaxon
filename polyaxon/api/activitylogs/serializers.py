from rest_framework import serializers

from db.models.activitylogs import ActivityLog


class ActivityLogsSerializer(serializers.ModelSerializer):
    object_name = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = ['id', 'event_type', 'actor', 'created_at', 'object_id', 'object_name']

    def get_object_name(self, obj):
        # Deleted objects don't have a content object any more
        if not obj.content_object:
            return None
        if hasattr(obj.content_object, 'unique_name'):
            return obj.content_object.unique_name
        if hasattr(obj.content_object, 'name'):
            return obj.content_object.name
        return None
