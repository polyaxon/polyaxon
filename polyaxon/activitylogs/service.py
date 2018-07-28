from activitylogs.manager import default_manager
from constants import user_system
from event_manager.event_service import EventService


class ActivityLogService(EventService):
    event_manager = default_manager

    def __init__(self):
        self.activity_log = None

    def record_event(self, event):
        assert event.actor_id is not None
        actor_id = event.data[event.actor_id]
        return self.activity_log.objects.create(
            event_type=event.event_type,
            actor_id=actor_id if actor_id != user_system.USER_SYSTEM_ID else None,
            context=event.data,
            created_at=event.datetime,
            content_object=event.instance,
        )

    def setup(self):
        super().setup()
        # Load default event types
        import activitylogs.events  # noqa

        from db.models.activitylogs import ActivityLog

        self.activity_log = ActivityLog
