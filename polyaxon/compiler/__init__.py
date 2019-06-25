from hestia.service_interface import LazyServiceWrapper

from compiler.service import CompilerService

backend = LazyServiceWrapper(
    backend_base=CompilerService,
    backend_path='compiler.service.CompilerService',
    options={}
)
backend.expose(locals())
