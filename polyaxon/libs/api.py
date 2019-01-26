from typing import Optional

from django.conf import settings

from polyaxon.config_manager import config

API_HTTP_URL = 'POLYAXON_API_HTTP_HOST'
API_WS_HOST = 'POLYAXON_API_WS_HOST'


def get_settings_http_api_url() -> str:
    return '{}://{}:{}'.format(settings.PROTOCOL,
                               settings.POLYAXON_K8S_API_HOST,
                               80)


def get_settings_ws_api_url() -> str:
    return '{}://{}:{}'.format(settings.PROTOCOL,
                               settings.POLYAXON_K8S_API_HOST,
                               1337)


def get_settings_external_http_api_url() -> str:
    return '{}://{}:{}'.format(settings.PROTOCOL,
                               settings.POLYAXON_K8S_API_HOST,
                               settings.POLYAXON_K8S_API_HTTP_PORT)


def get_settings_external_ws_api_url() -> str:
    return '{}://{}:{}'.format(settings.PROTOCOL,
                               settings.POLYAXON_K8S_API_HOST,
                               settings.POLYAXON_K8S_API_WS_PORT)


def get_http_api_url() -> Optional[str]:
    return config.get_string(API_HTTP_URL, is_optional=True)


def get_ws_api_url() -> Optional[str]:
    return config.get_string(API_WS_HOST, is_optional=True)
