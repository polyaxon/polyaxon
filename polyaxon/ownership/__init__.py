from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from ownership.exceptions import OwnershipError
from ownership.service import OwnershipService


def get_ownership_backend():
    if not settings.OWNERSHIP_BACKEND:
        return 'ownership.service.OwnershipService'
    raise OwnershipError()


backend = LazyServiceWrapper(
    backend_base=OwnershipService,
    backend_path=get_ownership_backend(),
    options={}
)
backend.expose(locals())
