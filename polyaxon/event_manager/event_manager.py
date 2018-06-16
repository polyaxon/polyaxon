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
