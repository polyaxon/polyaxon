class ManagerInterface(object):
    def __init__(self):
        self._state = {}

    @property
    def state(self):
        return self._state

    def _get_state_data(self, obj):
        raise NotImplementedError

    def subscribe(self, obj):
        key, value = self._get_state_data(obj)
        self._subscribe(key=key, value=value)

    def _subscribe(self, key, value):
        if key in self._state:
            assert self._state[key] == value
        else:
            self._state[key] = value

    def knows(self, key):
        return key in self._state

    def get(self, key):
        return self._state.get(key)
