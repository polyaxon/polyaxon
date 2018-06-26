import json

from django.conf import settings
from kubernetes import client

from libs.api import API_KEY_NAME, get_settings_api_url
from scheduler.spawners.templates import constants


def get_env_var(name, value, reraise=True):
    if not isinstance(value, str):
        try:
            value = json.dumps(value)
        except (ValueError, TypeError) as e:
            if reraise:
                raise e

    return client.V1EnvVar(name=name, value=value)


def get_from_app_secret(key_name, secret_key_name, secret_ref_name=None):
    secret_ref_name = secret_ref_name or settings.POLYAXON_K8S_APP_SECRET_NAME
    secret_key_ref = client.V1SecretKeySelector(name=secret_ref_name, key=secret_key_name)
    value_from = client.V1EnvVarSource(secret_key_ref=secret_key_ref)
    return client.V1EnvVar(name=key_name, value_from=value_from)


def get_service_env_vars(namespace='default'):
    return [
        get_env_var(name='POLYAXON_K8S_NAMESPACE', value=namespace),
        get_from_app_secret('POLYAXON_SECRET_KEY', 'polyaxon-secret'),
        get_from_app_secret('POLYAXON_INTERNAL_SECRET_TOKEN', 'polyaxon-internal-secret-token'),
        get_from_app_secret('POLYAXON_RABBITMQ_PASSWORD', 'rabbitmq-password',
                            settings.POLYAXON_K8S_RABBITMQ_SECRET_NAME),
        get_env_var(name=API_KEY_NAME, value=get_settings_api_url()),
    ]


def get_job_env_vars(log_level, outputs_path, logs_path, data_path, project_data_path=None):
    return [
        get_env_var(name=constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME, value=log_level),
        get_env_var(name=API_KEY_NAME, value=get_settings_api_url()),
        get_env_var(name=constants.CONFIG_MAP_RUN_OUTPUTS_PATH_KEY_NAME, value=outputs_path),
        get_env_var(name=constants.CONFIG_MAP_RUN_LOGS_PATH_KEY_NAME, value=logs_path),
        get_env_var(name=constants.CONFIG_MAP_RUN_DATA_PATH_KEY_NAME, value=data_path),
        get_env_var(name=constants.CONFIG_MAP_PROJECT_DATA_PATH_KEY_NAME, value=project_data_path),
        get_from_app_secret('POLYAXON_INTERNAL_SECRET_TOKEN', 'polyaxon-internal-secret-token'),
    ]


def get_resources_env_vars(resources):
    env_vars = []
    if resources:
        if resources.gpu and settings.LD_LIBRARY_PATH:
            env_vars += [client.V1EnvVar(name='LD_LIBRARY_PATH', value=settings.LD_LIBRARY_PATH)]
        if resources.gpu and not settings.LD_LIBRARY_PATH:
            # TODO: logger.warning('`LD_LIBRARY_PATH` was not properly set.')  # Publish error
            pass

    # Fix https://github.com/kubernetes/kubernetes/issues/59629
    # When resources.gpu.limits is not set or set to 0, we explicitly
    # pass NVIDIA_VISIBLE_DEVICES=none into container to avoid exposing GPUs.
    if (not resources or not resources.gpu or
            not resources.gpu.limits or resources.gpu.limits == '0'):
        env_vars.append(
            client.V1EnvVar(
                name='NVIDIA_VISIBLE_DEVICES',
                value='none'
            )
        )

    return env_vars
