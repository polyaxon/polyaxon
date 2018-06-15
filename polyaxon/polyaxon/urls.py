from polyaxon.config_manager import config

urlpatterns = []

if config.is_monolith_service or config.is_api_service:
    from api.patterns import *  # noqa
