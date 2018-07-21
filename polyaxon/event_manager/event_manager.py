from event_manager import event_actions
from libs.managers import ManagerInterface


class EventManager(ManagerInterface):

    def _get_state_data(self, event):  # pylint:disable=arguments-differ
        return event.event_type, event

    def subscribe(self, event):  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeEvent)
        """
        super().subscribe(obj=event)

    def knows(self, event_type):  # pylint:disable=arguments-differ
        return super().knows(key=event_type)

    def get(self, event_type):  # pylint:disable=arguments-differ
        return super().get(key=event_type)

    def user_write_events(self):
        """Return event types where use acted on an object.

        The write events are events with actions:
            * CREATED
            * UPDATED
            * DELETED
            * RESUMED
            * COPIED
            * CLONED
            * STOPPED
        """
        return [event_type for event_type, event in self.items if event.get_event_action()
                in event_actions.WRITE_ACTIONS]
