class EventManager(object):
    def __init__(self):
        self._event_types = {}

    def register(self, event_cls):
        """
        >>> register(SomeEvent)
        """
        event_type = event_cls.event_type
        if event_type in self._event_types:
            assert self._event_types[event_type] == event_cls
        else:
            self._event_types[event_type] = event_cls

    def get(self, event_type):
        return self._event_types[event_type]
