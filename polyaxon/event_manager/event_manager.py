from libs.managers import ManagerInterface


class EventManager(ManagerInterface):

    def _get_state_data(self, event):  # pylint:disable=arguments-differ
        return event.event_type, event

    def subscribe(self, event):  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeEvent)
        """
        super(EventManager, self).subscribe(obj=event)

    def knows(self, event_type):  # pylint:disable=arguments-differ
        return super(EventManager, self).knows(key=event_type)

    def get(self, event_type):  # pylint:disable=arguments-differ
        return super(EventManager, self).get(key=event_type)
