import analytics
from auditor.manager import default_manager
from libs.event_manager.event import Event
from libs.event_manager.event_service import EventService


class AuditorService(EventService):
    """An service that just passes the event to author services."""
    __all__ = ('record', 'validate')

    event_manager = default_manager
    EventModel = Event

    def get_event(self, event_type, instance, **kwargs):
        return {
            'event_type': event_type,
            'instance': instance,
            'kwargs': kwargs
        }

    def record_event(self, event):
        analytics.record(event_type=event['event_type'],
                         instance=event['instance'],
                         **event['kwargs'])

    def setup(self):
        # Load default event types
        import auditor.events  # NOQA
