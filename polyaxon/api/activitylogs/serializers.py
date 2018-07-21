from rest_framework import serializers

from db.models.activitylogs import ActivityLog
from event_manager import event_context


class ActivityLogsSerializer(serializers.ModelSerializer):
    object_name = serializers.SerializerMethodField()
    event_action = serializers.SerializerMethodField()
    event_subject = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = [
            'id',
            'event_action',
            'event_subject',
            'actor',
            'created_at',
            'object_id',
            'object_name'
        ]

    def get_event_action(self, obj):
        return event_context.get_event_action(event_type=obj.event_type)

    def get_event_subject(self, obj):
        return event_context.get_event_subject(event_type=obj.event_type)

    def get_object_name(self, obj):
        # Deleted objects don't have a content object any more
        if not obj.content_object:
            return None
        if hasattr(obj.content_object, 'unique_name'):
            return obj.content_object.unique_name
        if hasattr(obj.content_object, 'name'):
            return obj.content_object.name
        return None
