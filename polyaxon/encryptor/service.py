from hestia.service_interface import Service

from encryptor.manager import EncryptionManager
from options.registry.core import ENCRYPTION_KEY, ENCRYPTION_SECRET


class EncryptionService(Service):
    __all__ = ('encrypt', 'decrypt',)

    def __init__(self):
        self._manager = None

    def encrypt(self, value: str) -> str:
        return self._manager.encrypt(value)

    def decrypt(self, value: str) -> str:
        return self._manager.decrypt(value)

    def delete(self, name: str) -> None:
        delattr(self._settings, name)

    def setup(self) -> None:
        super().setup()
        import conf

        self._manager = EncryptionManager(key=conf.get(ENCRYPTION_KEY),
                                          secret=conf.get(ENCRYPTION_SECRET))
