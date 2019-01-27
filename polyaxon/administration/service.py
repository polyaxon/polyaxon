from typing import List

from hestia.service_interface import Service


class AdminService(Service):

    def __init__(self, models: List[str] = None) -> None:
        self._models = models

    def setup(self) -> None:
        super().setup()

        from administration.register import register

        register(self._models)
