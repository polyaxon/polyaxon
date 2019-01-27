from typing import Dict

from auditor.manager import default_manager
from event_manager.event import Event
from event_manager.event_service import EventService


class AuditorService(EventService):
    """An service that just passes the event to author services."""
    __all__ = EventService.__all__ + ('log', 'notify', 'track')

    event_manager = default_manager

    def __init__(self):
        self.activitylogs = None
        self.executor = None
        self.notifier = None
        self.tracker = None
        self.ref_id = None

    def get_ref_id(self) -> str:
        if self.ref_id:
            return self.ref_id

        from db.models.clusters import Cluster
        from django.db import InterfaceError, OperationalError, ProgrammingError
        try:
            self.ref_id = Cluster.load().uuid
        except (Cluster.DoesNotExist, InterfaceError, ProgrammingError, OperationalError):
            pass
        return self.ref_id

    def record_event(self, event: Event) -> None:
        """
        Record the event async.
        """
        from polyaxon.celery_api import celery_app
        from polyaxon.settings import EventsCeleryTasks

        if not event.ref_id:
            event.ref_id = self.get_ref_id()
        serialized_event = event.serialize(dumps=False,
                                           include_actor_name=True,
                                           include_instance_info=True)

        celery_app.send_task(EventsCeleryTasks.EVENTS_TRACK, kwargs={'event': serialized_event})
        celery_app.send_task(EventsCeleryTasks.EVENTS_LOG, kwargs={'event': serialized_event})
        celery_app.send_task(EventsCeleryTasks.EVENTS_NOTIFY, kwargs={'event': serialized_event})
        # We include the instance in the serialized event for executor
        serialized_event['instance'] = event.instance
        self.executor.record(event_type=event.event_type, event_data=serialized_event)

    def notify(self, event: Dict) -> None:
        self.notifier.record(event_type=event['type'], event_data=event)

    def track(self, event: Dict) -> None:
        self.tracker.record(event_type=event['type'], event_data=event)

    def log(self, event: Dict) -> None:
        self.activitylogs.record(event_type=event['type'], event_data=event)

    def setup(self) -> None:
        super().setup()
        # Load default event types
        import auditor.events  # noqa

        import activitylogs
        import executor
        import notifier
        import tracker

        self.notifier = notifier
        self.tracker = tracker
        self.activitylogs = activitylogs
        self.executor = executor
