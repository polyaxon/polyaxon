from event_manager.event import Event
from event_manager.event_service import EventService
from tracker.manager import default_manager


class AnalyticService(EventService):
    __all__ = ('record', 'validate')

    event_manager = default_manager
    EventModel = Event

    def setup(self):
        # Load default event types
        import tracker.events  # noqa
