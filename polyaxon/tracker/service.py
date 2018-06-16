from event_manager.event_service import EventService
from tracker.manager import default_manager


class TrackerService(EventService):

    event_manager = default_manager

    def setup(self):
        super().setup()
        # Load default event types
        import tracker.events  # noqa
