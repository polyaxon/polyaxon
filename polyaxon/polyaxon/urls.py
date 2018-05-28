from polyaxon.utils import config

urlpatterns = []

if config.is_monolith_service or config.is_api_service:
    from django.urls import include, re_path
    from api.patterns import *
    urlpatterns = [
        re_path(r'', include('api.patterns')),
    ]
