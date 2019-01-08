from hestia.service_interface import Service


class AdminService(Service):

    def __init__(self, models=None):
        self._models = models

    def setup(self):
        super().setup()

        from administration.register import register

        register(self._models)
