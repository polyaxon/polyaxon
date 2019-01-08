from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from administration.service import AdminService


def get_admin_backend():
    return settings.ADMIN_BACKEND or 'administration.service.AdminService'


backend = LazyServiceWrapper(
    backend_base=AdminService,
    backend_path=get_admin_backend(),
    options={}
)
backend.expose(locals())
