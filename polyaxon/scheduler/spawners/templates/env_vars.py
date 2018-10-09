import json

from kubernetes import client

from django.conf import settings

from constants.urls import VERSION_V1
from db.models.outputs import get_paths_from_specs
from libs.api import API_HTTP_URL, API_WS_HOST, get_settings_http_api_url, get_settings_ws_api_url
from scheduler.spawners.templates import constants


def get_env_var(name, value, reraise=True):
    if not isinstance(value, str):
        try:
            value = json.dumps(value)
        except (ValueError, TypeError) as e:
            if reraise:
                raise e

    return client.V1EnvVar(name=name, value=value)


def get_from_secret(key_name, secret_key_name, secret_ref_name=None):
    secret_ref_name = secret_ref_name or settings.POLYAXON_K8S_APP_SECRET_NAME
    secret_key_ref = client.V1SecretKeySelector(name=secret_ref_name, key=secret_key_name)
    value_from = client.V1EnvVarSource(secret_key_ref=secret_key_ref)
    return client.V1EnvVar(name=key_name, value_from=value_from)


def get_service_env_vars(namespace='default'):
    return [
        get_env_var(name='POLYAXON_K8S_NAMESPACE', value=namespace),
        get_from_secret('POLYAXON_SECRET_KEY', 'POLYAXON_SECRET_KEY'),
        get_from_secret('POLYAXON_SECRET_INTERNAL_TOKEN', 'POLYAXON_SECRET_INTERNAL_TOKEN'),
        get_from_secret('POLYAXON_RABBITMQ_PASSWORD', 'rabbitmq-password',
                        settings.POLYAXON_K8S_RABBITMQ_SECRET_NAME),
        get_from_secret('POLYAXON_DB_PASSWORD', 'postgres-password',
                        settings.POLYAXON_K8S_DB_SECRET_NAME),
        get_env_var(name=API_HTTP_URL, value=get_settings_http_api_url()),
        get_env_var(name=API_WS_HOST, value=get_settings_ws_api_url()),
        get_env_var(name=constants.CONFIG_MAP_IN_CLUSTER, value=True),
        get_env_var(name=constants.CONFIG_MAP_API_VERSION, value=VERSION_V1),
    ]


def get_job_env_vars(outputs_path,
                     data_paths,
                     log_level=None,
                     logs_path=None,
                     outputs_refs_jobs=None,
                     outputs_refs_experiments=None,
                     ephemeral_token=None):
    env_vars = [
        get_env_var(name=API_HTTP_URL, value=get_settings_http_api_url()),
        get_env_var(name=API_WS_HOST, value=get_settings_ws_api_url()),
        get_env_var(name=constants.CONFIG_MAP_IN_CLUSTER, value=True),
        get_env_var(name=constants.CONFIG_MAP_API_VERSION, value=VERSION_V1),
        get_env_var(name=constants.CONFIG_MAP_INTERNAL_HEADER,
                    value=settings.HEADERS_INTERNAL.replace('_', '-')),
        get_env_var(name=constants.CONFIG_MAP_INTERNAL_HEADER_SERVICE,
                    value=settings.INTERNAL_SERVICES.RUNNER),
        get_env_var(name=constants.CONFIG_MAP_RUN_OUTPUTS_PATH_KEY_NAME, value=outputs_path),
        get_env_var(name=constants.CONFIG_MAP_RUN_DATA_PATHS_KEY_NAME, value=data_paths),
    ]
    if log_level:
        env_vars.append(
            get_env_var(name=constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME, value=log_level))

    if logs_path:
        env_vars.append(
            get_env_var(name=constants.CONFIG_MAP_RUN_LOGS_PATH_KEY_NAME, value=logs_path))

    refs_outputs = {}
    outputs_jobs_paths = get_paths_from_specs(specs=outputs_refs_jobs)
    if outputs_jobs_paths:
        refs_outputs['jobs'] = outputs_jobs_paths
    outputs_experiments_paths = get_paths_from_specs(specs=outputs_refs_experiments)
    if outputs_experiments_paths:
        refs_outputs['experiments'] = outputs_experiments_paths
    if refs_outputs:
        env_vars.append(
            get_env_var(name=constants.CONFIG_MAP_REFS_OUTPUTS_PATHS_KEY_NAME,
                        value=refs_outputs))
    if ephemeral_token:
        env_vars.append(
            get_env_var(name=constants.SECRET_EPHEMERAL_TOKEN,
                        value=ephemeral_token))
    return env_vars


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
    condition = (not resources or
                 not resources.gpu or
                 not resources.gpu.limits or
                 resources.gpu.limits == '0')
    if condition:
        env_vars.append(
            client.V1EnvVar(
                name='NVIDIA_VISIBLE_DEVICES',
                value='none'
            )
        )

    return env_vars


class EnvFromRefFoundError(Exception):
    pass


def validate_secret_refs(secret_refs):
    for secret_ref in secret_refs or []:
        if secret_ref not in settings.REFS_SECRETS:
            raise EnvFromRefFoundError('secret_ref with name `{}` was defined in specification, '
                                       'but was not found'.format(secret_ref))
    return secret_refs


def validate_configmap_refs(configmap_refs):
    for configmap_ref in configmap_refs or []:
        if configmap_ref not in settings.REFS_CONFIG_MAPS:
            raise EnvFromRefFoundError('configmap_ref with name `{}` was defined in specification, '
                                       'but was not found'.format(configmap_ref))
    return configmap_refs


def get_env_from(secret_ref=None, config_map_ref=None):
    if not any([secret_ref, config_map_ref]) or all([secret_ref, config_map_ref]):
        raise ValueError('One and only one value is required for get_env_from.')

    if secret_ref:
        return client.V1EnvFromSource(secret_ref={'name': secret_ref})
    return client.V1EnvFromSource(config_map_ref={'name': config_map_ref})


def get_pod_env_from(secret_refs=None, configmap_refs=None):
    secret_refs = secret_refs or []
    configmap_refs = configmap_refs or []
    env_from = []
    env_from += [get_env_from(secret_ref=secret_ref) for secret_ref in secret_refs]
    env_from += [get_env_from(config_map_ref=configmap_ref) for configmap_ref in configmap_refs]
    return env_from
