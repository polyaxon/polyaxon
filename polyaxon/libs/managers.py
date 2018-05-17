class ManagerInterface(object):
    def __init__(self):
        self._state = {}

    @property
    def state(self):
        return self._state

    def subscribe(self, *args):
        raise NotImplementedError

    def knows(self, key):
        return key in self._state

    def get(self, key):
        return self._state.get(key)
