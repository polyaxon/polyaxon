from typing import Optional

import conf

from db.models.registry_access import RegistryAccess
from options.registry.access import ACCESS_REGISTRY
from options.registry.registries import REGISTRY_HOST, REGISTRY_IN_CLUSTER, REGISTRY_LOCALHOST
from registry.exceptions import ContainerRegistryError
from registry.spec import RegistryContextSpec
from schemas import BuildBackend


def get_in_cluster_registry_host(build_backend: Optional[str]) -> str:
    if build_backend in {BuildBackend.NATIVE, None}:
        return conf.get(REGISTRY_LOCALHOST)
    return conf.get(REGISTRY_HOST)


def get_in_cluster_registry_spec(build_backend: Optional[str]) -> RegistryContextSpec:
    host = get_in_cluster_registry_host(build_backend)
    return RegistryContextSpec(host=host, secret=None, secret_items=None, insecure=True)


def get_registry_spec_from_config(config: 'RegistryAccess') -> RegistryContextSpec:
    return RegistryContextSpec(host=config.host,
                               secret=config.k8s_secret.k8s_ref,
                               secret_items=config.k8s_secret.items,
                               insecure=config.insecure)


def get_registry_context(build_backend: Optional[str]) -> RegistryContextSpec:
    registry_config = RegistryAccess.objects.filter(id=conf.get(ACCESS_REGISTRY))
    if registry_config.exists():
        registry_config = registry_config.last()
        return get_registry_spec_from_config(registry_config)

    if conf.get(REGISTRY_IN_CLUSTER):
        return get_in_cluster_registry_spec(build_backend=build_backend)

    raise ContainerRegistryError('Please check your registry configuration.')
