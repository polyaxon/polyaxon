from event_manager.event_service import EventService
from tracker.manager import default_manager


class TrackerService(EventService):
    __all__ = ('record', 'validate')

    event_manager = default_manager

    def setup(self):
        # Load default event types
        import tracker.events  # noqa
