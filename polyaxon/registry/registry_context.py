from typing import Optional

import conf

from registry.exceptions import ContainerRegistryError
from registry.spec import RegistryContextSpec
from db.models.configs import Config
from options.registry.registries import REGISTRY_HOST, REGISTRY_IN_CLUSTER, REGISTRY_LOCALHOST
from schemas import BuildBackend


def get_in_cluster_registry_host(build_backend: Optional[str]) -> str:
    if build_backend in {BuildBackend.NATIVE, None}:
        return conf.get(REGISTRY_LOCALHOST)
    return conf.get(REGISTRY_HOST)


def get_in_cluster_registry_spec(build_backend: Optional[str]) -> RegistryContextSpec:
    host = get_in_cluster_registry_host(build_backend)
    return RegistryContextSpec(host=host, secret=None, secret_keys=None, insecure=True)


def get_registry_spec_from_config(config: 'RegistryAccess') -> RegistryContextSpec:
    return RegistryContextSpec(host=config.host,
                               secret=config.k8s_secrets.secret_ref,
                               secret_keys=config.k8s_secrets.keys,
                               insecure=config.insecure)


def get_registry_context(build_backend: Optional[str]) -> RegistryContextSpec:
    # TODO: add tests
    config = Config.objects.prefetch_related('registry_access').last()
    if config and config.registry_access:
        registry_config = config.registry_access
        return get_registry_spec_from_config(registry_config)

    if conf.get(REGISTRY_IN_CLUSTER):
        return get_in_cluster_registry_spec(build_backend=build_backend)

    raise ContainerRegistryError('Please check your registry configuration.')
