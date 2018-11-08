from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from ownership.exceptions import OwnershipError
from ownership.service import OwnershipService


def get_ownership_backend():
    if not settings.OWNERSHIP_BACKEND or not settings.OWNERSHIP_BACKENDS:
        return 'ownership.service.OwnershipService'
    if settings.OWNERSHIP_BACKENDS not in settings.OWNERSHIP_BACKENDS:
        raise OwnershipError()
    return settings.OWNERSHIP_BACKENDS[settings.OWNERSHIP_BACKEND]


backend = LazyServiceWrapper(
    backend_base=OwnershipService,
    backend_path=get_ownership_backend(),
    options={}
)
backend.expose(locals())
