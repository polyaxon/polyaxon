from django.conf import settings

from scheduler.spawners.templates.env_vars import get_from_app_secret


def get_service_env_vars():
    return [
        get_from_app_secret('POLYAXON_SECRET_KEY', 'polyaxon-secret'),
        get_from_app_secret('POLYAXON_INTERNAL_SECRET_TOKEN', 'polyaxon-internal-secret-token'),
        get_from_app_secret('POLYAXON_RABBITMQ_PASSWORD', 'rabbitmq-password',
                            settings.POLYAXON_K8S_RABBITMQ_SECRET_NAME)
    ]
