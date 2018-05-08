from analytics.manager import default_manager
from event_manager.event import Event
from event_manager.event_service import EventService


class AnalyticService(EventService):
    __all__ = ('record', 'validate')

    event_manager = default_manager
    EventModel = Event

    def setup(self):
        # Load default event types
        pass
