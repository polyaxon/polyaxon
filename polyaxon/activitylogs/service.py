from activitylogs.models import ActivityLog
from event_manager.event_service import EventService
from tracker.manager import default_manager


class ActivityLogService(EventService):

    event_manager = default_manager

    def record_event(self, event):
        return ActivityLog.objects.create(
            event=event.event_type,
            actor_id=event.data['id'],
            context=event.data,
            # content_type=content_type_mapping[event.get_event_subject()],
            object_id=event.data['id']
        )

    def setup(self):
        # Load default event types
        import activitylogs.events  # noqa
