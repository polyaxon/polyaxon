from django.conf import settings

from polyaxon.utils import config

API_KEY_NAME = 'POLYAXON_API'


def get_settings_api_url():
    return '{}://{}:{}'.format(settings.PROTOCOL,
                              settings.POLYAXON_K8S_API_HOST,
                              settings.POLYAXON_K8S_API_PORT)


def get_service_api_url():
    return config.get_string(API_KEY_NAME, is_optional=True)
