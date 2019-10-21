from typing import Optional

import conf

from db.models.registry_access import RegistryAccess
from options.registry.access import ACCESS_REGISTRY
from options.registry.registries import REGISTRY_HOST, REGISTRY_IN_CLUSTER, REGISTRY_LOCALHOST
from registry.exceptions import ContainerRegistryError
from registry.spec import RegistryContextSpec
from schemas import BuildBackend


def get_in_cluster_registry_host(build_backend: Optional[str]) -> str:
    if build_backend == BuildBackend.NATIVE or not build_backend:
        return conf.get(REGISTRY_LOCALHOST)
    return conf.get(REGISTRY_HOST)


def get_in_cluster_registry_spec(build_backend: Optional[str],
                                 secret=None,
                                 secret_items=None) -> RegistryContextSpec:
    host = get_in_cluster_registry_host(build_backend)
    return RegistryContextSpec(host=host, secret=secret, secret_items=secret_items, insecure=True)


def get_registry_spec_from_config(config: 'RegistryAccess') -> RegistryContextSpec:
    return RegistryContextSpec(host=config.host,
                               secret=config.k8s_secret.k8s_ref if config.k8s_secret else None,
                               secret_items=config.k8s_secret.items if config.k8s_secret else None,
                               insecure=config.insecure)


def get_registry_context(build_backend: Optional[str]) -> RegistryContextSpec:
    registry_config = RegistryAccess.objects.filter(id=conf.get(ACCESS_REGISTRY)).last()
    if registry_config:

        # The default registry has no host
        if not registry_config.host:
            if conf.get(REGISTRY_IN_CLUSTER):
                secret = None
                secret_items = None
                if registry_config.k8s_secret:
                    secret = registry_config.k8s_secret.k8s_ref
                    secret_items = registry_config.k8s_secret.items
                return get_in_cluster_registry_spec(
                    build_backend=build_backend, secret=secret, secret_items=secret_items)
            else:
                raise ContainerRegistryError('The default registry has no host defined.')

        return get_registry_spec_from_config(registry_config)

    if conf.get(REGISTRY_IN_CLUSTER):
        return get_in_cluster_registry_spec(build_backend=build_backend)

    raise ContainerRegistryError('Please check your registry configuration.')
