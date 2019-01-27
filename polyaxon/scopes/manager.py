class ScopeMappingManager(object):
    def __init__(self, config):
        self._config = config
        self._default = {
            'HEAD': (),
            'GET': (),
            'POST': (),
            'PUT': (),
            'PATCH': (),
            'DELETE': (),
        }

    def get(self, endpoint: str):
        return self._config.get(endpoint, self._default)
