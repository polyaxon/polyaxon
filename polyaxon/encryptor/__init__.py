from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from encryptor.service import EncryptionService


def get_conf_backend():
    return settings.ENCRYPTION_BACKEND or 'encryptor.service.EncryptionService'


backend = LazyServiceWrapper(
    backend_base=EncryptionService,
    backend_path=get_conf_backend(),
    options={}
)
backend.expose(locals())
