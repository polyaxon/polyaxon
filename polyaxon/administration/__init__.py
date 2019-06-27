from hestia.service_interface import LazyServiceWrapper

from django.conf import settings

from administration.service import AdminService


def get_admin_backend():
    return settings.ADMIN_BACKEND or 'administration.service.AdminService'


def get_admin_options():
    return {'models': settings.ADMIN_MODELS}


backend = LazyServiceWrapper(
    backend_base=AdminService,
    backend_path=get_admin_backend(),
    options=get_admin_options()
)
backend.expose(locals())
