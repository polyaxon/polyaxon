import tracker

from auditor.manager import default_manager
from event_manager.event_service import EventService


class AuditorService(EventService):
    """An service that just passes the event to author services."""

    event_manager = default_manager

    def get_event(self, event_type, instance, **kwargs):
        return {
            'event_type': event_type,
            'instance': instance,
            'kwargs': kwargs
        }

    def record_event(self, event):
        tracker.record(event_type=event['event_type'],
                       instance=event['instance'],
                       **event['kwargs'])

    def setup(self):
        # Load default event types
        import auditor.events  # noqa
