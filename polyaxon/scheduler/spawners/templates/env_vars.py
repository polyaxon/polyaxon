import json

from hestia.internal_services import InternalServices
from kubernetes import client

from django.conf import settings

import conf
import stores

from constants.urls import VERSION_V1
from db.models.config_maps import K8SConfigMap
from db.models.outputs import get_paths_from_specs
from db.models.secrets import K8SSecret
from libs.api import API_HTTP_URL, API_WS_HOST, get_settings_http_api_url, get_settings_ws_api_url
from options.registry.core import HEADERS_INTERNAL
from scheduler.spawners.templates import constants
from scheduler.spawners.templates.stores import (
    get_data_store_secrets,
    get_outputs_refs_store_secrets,
    get_outputs_store_secrets
)


def get_env_var(name, value, reraise=True):
    if not isinstance(value, str):
        try:
            value = json.dumps(value)
        except (ValueError, TypeError) as e:
            if reraise:
                raise e

    return client.V1EnvVar(name=name, value=value)


def get_from_field_ref(name, field_path):
    field_ref = client.V1ObjectFieldSelector(field_path=field_path)
    value_from = client.V1EnvVarSource(field_ref=field_ref)
    return client.V1EnvVar(name=name, value_from=value_from)


def get_from_config_map(key_name, cm_key_name, config_map_ref_name=None):
    config_map_ref_name = config_map_ref_name or settings.POLYAXON_K8S_APP_CONFIG_NAME
    config_map_key_ref = client.V1ConfigMapKeySelector(name=config_map_ref_name, key=cm_key_name)
    value_from = client.V1EnvVarSource(config_map_key_ref=config_map_key_ref)
    return client.V1EnvVar(name=key_name, value_from=value_from)


def get_from_secret(key_name, secret_key_name, secret_ref_name=None):
    secret_ref_name = secret_ref_name or settings.POLYAXON_K8S_APP_SECRET_NAME
    secret_key_ref = client.V1SecretKeySelector(name=secret_ref_name, key=secret_key_name)
    value_from = client.V1EnvVarSource(secret_key_ref=secret_key_ref)
    return client.V1EnvVar(name=key_name, value_from=value_from)


def get_internal_env_vars(service_internal_header,
                          namespace='default',
                          include_secret_key=False,
                          include_internal_token=False,
                          authentication_type=None):
    env_vars = [
        get_env_var(name='POLYAXON_K8S_NAMESPACE', value=namespace),
        get_env_var(name=API_HTTP_URL, value=get_settings_http_api_url()),
        get_env_var(name=API_WS_HOST, value=get_settings_ws_api_url()),
        get_env_var(name=constants.CONFIG_MAP_IN_CLUSTER, value=True),
        get_env_var(name=constants.CONFIG_MAP_IS_MANAGED, value=True),
        get_env_var(name=constants.CONFIG_MAP_API_VERSION, value=VERSION_V1),
        get_env_var(name=constants.CONFIG_MAP_INTERNAL_HEADER,
                    value=conf.get(HEADERS_INTERNAL).replace('_', '-')),
        get_env_var(name=constants.CONFIG_MAP_INTERNAL_HEADER_SERVICE,
                    value=service_internal_header),
    ]
    if include_secret_key:
        env_vars.append(
            get_from_secret('POLYAXON_SECRET_KEY', 'POLYAXON_SECRET_KEY'),)
    if include_internal_token:
        env_vars.append(
            get_from_secret('POLYAXON_SECRET_INTERNAL_TOKEN', 'POLYAXON_SECRET_INTERNAL_TOKEN'),)
    if authentication_type:
        env_vars.append(
            get_env_var(name='POLYAXON_AUTHENTICATION_TYPE', value=authentication_type))
    return env_vars


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
        get_env_var(name=constants.CONFIG_MAP_IS_MANAGED, value=True),
        get_env_var(name=constants.CONFIG_MAP_API_VERSION, value=VERSION_V1),
    ]


def get_job_stores_secrets_env_vars(persistence_outputs,
                                    outputs_path,
                                    persistence_data,
                                    data_paths,
                                    outputs_refs_jobs=None,
                                    outputs_refs_experiments=None):
    env_vars = []

    # Stores' secrets
    secrets = set([])
    secret_items = {}
    data_secrets, data_secret_items = get_data_store_secrets(
        persistence_data=persistence_data, data_paths=data_paths)
    secrets |= data_secrets
    secret_items.update(data_secret_items)

    outputs_secrets, outputs_secret_items = get_outputs_store_secrets(
        persistence_outputs=persistence_outputs, outputs_path=outputs_path)
    secrets |= outputs_secrets
    secret_items.update(outputs_secret_items)

    jobs_refs_secrets, jobs_refs_secret_items = get_outputs_refs_store_secrets(
        specs=outputs_refs_jobs)
    secrets |= jobs_refs_secrets
    secret_items.update(jobs_refs_secret_items)

    experiments_refs_secrets, experiments_refs_secret_items = get_outputs_refs_store_secrets(
        specs=outputs_refs_experiments)
    secrets |= experiments_refs_secrets
    secret_items.update(experiments_refs_secret_items)

    # Expose secret keys from all secrets
    for (secret, secret_key) in secrets:
        env_vars.append(get_from_secret(key_name=secret_key,
                                        secret_key_name=secret_key,
                                        secret_ref_name=secret))
    # Add paths' secret env vars
    if secret_items:
        env_vars.append(
            get_env_var(name=constants.CONFIG_MAP_RUN_STORES_ACCESS_KEYS, value=secret_items))

    return env_vars


def get_job_env_vars(namespace,
                     persistence_outputs,
                     outputs_path,
                     persistence_data,
                     log_level=None,
                     logs_path=None,
                     outputs_refs_jobs=None,
                     outputs_refs_experiments=None,
                     ephemeral_token=None):
    env_vars = get_internal_env_vars(service_internal_header=InternalServices.RUNNER,
                                     namespace=namespace)
    if log_level:
        env_vars.append(
            get_env_var(name=constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME, value=log_level))

    if logs_path:
        env_vars.append(
            get_env_var(name=constants.CONFIG_MAP_RUN_LOGS_PATH_KEY_NAME, value=logs_path))

    # Data and outputs paths
    data_paths = stores.get_data_paths(persistence_data)
    env_vars += [
        get_env_var(name=constants.CONFIG_MAP_RUN_OUTPUTS_PATH_KEY_NAME, value=outputs_path),
        get_env_var(name=constants.CONFIG_MAP_RUN_DATA_PATHS_KEY_NAME, value=data_paths)
    ]

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

    env_vars += get_job_stores_secrets_env_vars(persistence_outputs=persistence_outputs,
                                                outputs_path=outputs_path,
                                                persistence_data=persistence_data,
                                                data_paths=data_paths,
                                                outputs_refs_jobs=outputs_refs_jobs,
                                                outputs_refs_experiments=outputs_refs_experiments)
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


def get_kv_env_vars(kv_env_vars):
    env_vars = []
    if not kv_env_vars:
        return env_vars

    for kv_env_var in kv_env_vars:
        env_vars.append(get_env_var(name=kv_env_var[0], value=kv_env_var[1]))

    return env_vars


class EnvFromRefFoundError(Exception):
    pass


def get_env_from(secret_ref=None, config_map_ref=None):
    if not any([secret_ref, config_map_ref]) or all([secret_ref, config_map_ref]):
        raise ValueError('One and only one value is required for get_env_from.')

    if secret_ref:
        return client.V1EnvFromSource(secret_ref={'name': secret_ref})
    return client.V1EnvFromSource(config_map_ref={'name': config_map_ref})


def get_items_from(items, secret_ref=None, config_map_ref=None):
    if not any([secret_ref, config_map_ref]) or all([secret_ref, config_map_ref]):
        raise ValueError('One and only one value is required for get_env_from.')

    items_from = []
    if secret_ref:
        for item in items:
            items_from.append(get_from_secret(key_name=item,
                                              secret_key_name=item,
                                              secret_ref_name=secret_ref))
        return items_from
    for item in items:
        items_from.append(get_from_config_map(key_name=item,
                                              cm_key_name=item,
                                              config_map_ref_name=config_map_ref))


def get_pod_env_from_secrets(secret_refs):
    if not secret_refs:
        return []
    secrets = K8SSecret.objects.filter(name__in=secret_refs)
    validation = set(secret_refs) - set([secret.name for secret in secrets])
    if validation:
        raise EnvFromRefFoundError(
            'The following secret refs `{}` '
            'were provided but not defined in the config maps catalog'.format(validation))

    env_from = []
    for secret in secrets:
        if secret.items:
            env_from.append(get_items_from(items=secret.items,
                                           secret_ref=secret.k8s_ref))
        else:
            env_from.append(get_env_from(secret_ref=secret.k8s_ref))
    return env_from


def get_pod_env_from_config_maps(config_map_refs):
    if not config_map_refs:
        return []
    config_maps = K8SConfigMap.objects.filter(name__in=config_map_refs)
    validation = set(config_map_refs) - set([config_map.name for config_map in config_maps])
    if validation:
        raise EnvFromRefFoundError(
            'The following config map refs `{}` '
            'were provided but not defined in the config maps catalog'.format(validation))

    env_from = []
    for config_map in config_maps:
        if config_map.items:
            env_from.append(get_items_from(items=config_map.items,
                                           config_map_ref=config_map.k8s_ref))
        else:
            env_from.append(get_env_from(config_map_ref=config_map.k8s_ref))
    return env_from


def get_pod_env_from(secret_refs=None, config_map_refs=None):
    secret_refs = secret_refs or []
    config_map_refs = config_map_refs or []
    env_from = []
    env_from += get_pod_env_from_secrets(secret_refs=secret_refs)
    env_from += get_pod_env_from_config_maps(config_map_refs=config_map_refs)
    return env_from
