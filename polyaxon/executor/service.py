from event_manager.event_service import EventService
from executor.manager import default_manager


class BaseExecutorService(EventService):

    event_manager = default_manager

    def setup(self) -> None:
        super().setup()
        # Load default event types
        import executor.events  # noqa
