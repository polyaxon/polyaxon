from typing import Dict, Optional

from activitylogs.manager import default_manager
from constants import user_system
from event_manager.event import Event
from event_manager.event_service import EventService


class ActivityLogService(EventService):
    event_manager = default_manager

    def __init__(self):
        self.activity_log_manager = None

    def record_event(self, event: Event) -> Optional[Dict]:
        if not event.ref_id:
            return
        assert event.actor_id is not None
        actor_id = event.data[event.actor_id]
        return self.activity_log_manager.create(
            ref=event.ref_id,
            event_type=event.event_type,
            actor_id=actor_id if actor_id != user_system.USER_SYSTEM_ID else None,
            context=event.data,
            created_at=event.datetime,
            object_id=event.instance_id,
            content_type_id=event.instance_contenttype
        )

    def setup(self) -> None:
        super().setup()
        # Load default event types
        import activitylogs.events  # noqa

        from db.models.activitylogs import ActivityLog

        self.activity_log_manager = ActivityLog.objects
