class EventManager(object):
    def __init__(self):
        self._event_by_types = {}

    def subscribe(self, event):
        """
        >>> subscribe(SomeEvent)
        """
        event_type = event.event_type
        if event_type in self._event_by_types:
            assert self._event_by_types[event_type] == event
        else:
            self._event_by_types[event_type] = event

    def knows(self, event_type):
        return event_type in self._event_by_types

    def get(self, event_type):
        return self._event_by_types.get(event_type)
