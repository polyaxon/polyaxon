from hestia.service_interface import LazyServiceWrapper

from ownership.exceptions import OwnershipError
from ownership.service import OwnershipService


backend = LazyServiceWrapper(
    backend_base=OwnershipService,
    backend_path='ownership.service.OwnershipService',
    options={}
)
backend.expose(locals())
