from libs.managers import ManagerInterface


class EventManager(ManagerInterface):

    def subscribe(self, event):
        """
        >>> subscribe(SomeEvent)
        """
        event_type = event.event_type
        if event_type in self._state:
            assert self._state[event_type] == event
        else:
            self._state[event_type] = event

    def knows(self, event_type):
        return super(EventManager, self).knows(key=event_type)

    def get(self, event_type):
        return super(EventManager, self).get(key=event_type)
