import pytest

from django.conf import settings
from django.test import override_settings

from db.models.clusters import Cluster
from db.models.configs import Config
from db.models.owner import Owner
from db.models.registry_access import RegistryAccess
from db.models.secrets import K8SSecret
from registry.exceptions import ContainerRegistryError
from registry.registry_context import (
    get_in_cluster_registry_host,
    get_in_cluster_registry_spec,
    get_registry_context,
    get_registry_spec_from_config
)
from registry.spec import RegistryContextSpec
from schemas import BuildBackend
from tests.base.case import BaseTest


@pytest.mark.dockerizer_mark
class TestRegistryContext(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def registry_spec(self):
        spec = RegistryContextSpec(host='https://some_host:5000',
                                   secret='docker-conf',
                                   secret_keys=None,
                                   insecure=False)
        assert spec.host == 'https://some_host:5000'
        assert spec.secret == 'docker-conf'
        assert spec.secret_keys is None
        assert spec.insecure is False

    def test_get_in_cluster_registry_host(self):
        settings.REGISTRY_LOCALHOST = 'registry_localhost'
        settings.REGISTRY_HOST = 'registry_host'

        assert get_in_cluster_registry_host(build_backend=None) == 'registry_localhost'
        assert get_in_cluster_registry_host(
            build_backend=BuildBackend.NATIVE) == 'registry_localhost'
        assert get_in_cluster_registry_host(
            build_backend=BuildBackend.KANIKO) == 'registry_host'

    @override_settings(REGISTRY_LOCALHOST='registry_localhost')
    @override_settings(REGISTRY_HOST='registry_host')
    def test_get_in_cluster_registry_spec(self):
        spec = get_in_cluster_registry_spec(build_backend=None)
        assert spec.host == 'registry_localhost'
        assert spec.secret is None
        assert spec.secret_keys is None
        assert spec.insecure is True

        spec = get_in_cluster_registry_spec(build_backend=BuildBackend.NATIVE)
        assert spec.host == 'registry_localhost'
        assert spec.secret is None
        assert spec.secret_keys is None
        assert spec.insecure is True

        spec = get_in_cluster_registry_spec(build_backend=BuildBackend.KANIKO)
        assert spec.host == 'registry_host'
        assert spec.secret is None
        assert spec.secret_keys is None
        assert spec.insecure is True

    def test_get_registry_spec_from_config(self):
        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='my_secret',
                                          secret_ref='my_secret')
        config = RegistryAccess.objects.create(owner=self.owner,
                                               host='https://index.docker.io/v1/foo',
                                               k8s_secret=secret,
                                               name='d-registry')
        spec = get_registry_spec_from_config(config=config)

        assert spec.host == 'https://index.docker.io/v1/foo'
        assert spec.secret == secret.secret_ref
        assert spec.secret_keys == secret.keys
        assert spec.insecure is False

    @override_settings(REGISTRY_IN_CLUSTER=False)
    def test_get_registry_context_no_config_not_in_cluster(self):
        with self.assertRaises(ContainerRegistryError):
            get_registry_context(build_backend=None)

        with self.assertRaises(ContainerRegistryError):
            get_registry_context(build_backend=BuildBackend.NATIVE)

        with self.assertRaises(ContainerRegistryError):
            get_registry_context(build_backend=BuildBackend.KANIKO)

    @override_settings(REGISTRY_LOCALHOST='registry_localhost')
    @override_settings(REGISTRY_HOST='registry_host')
    @override_settings(REGISTRY_IN_CLUSTER=True)
    def test_get_registry_context_in_cluster(self):
        spec = get_registry_context(build_backend=None)
        assert spec.host == 'registry_localhost'
        assert spec.secret is None
        assert spec.secret_keys is None
        assert spec.insecure is True

        spec = get_registry_context(build_backend=BuildBackend.NATIVE)
        assert spec.host == 'registry_localhost'
        assert spec.secret is None
        assert spec.secret_keys is None
        assert spec.insecure is True

        spec = get_registry_context(build_backend=BuildBackend.KANIKO)
        assert spec.host == 'registry_host'
        assert spec.secret is None
        assert spec.secret_keys is None
        assert spec.insecure is True

    @override_settings(REGISTRY_IN_CLUSTER=False)
    def test_get_external_registry_context(self):
        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='my_secret',
                                          secret_ref='my_secret')
        registry_access = RegistryAccess.objects.create(owner=self.owner,
                                                        host='https://index.docker.io/v1/foo',
                                                        k8s_secret=secret,
                                                        name='d-registry')
        Config.objects.create(owner=self.owner, registry_access=registry_access)

        spec = get_registry_context(build_backend=None)
        assert spec.host == 'https://index.docker.io/v1/foo'
        assert spec.secret == secret.secret_ref
        assert spec.secret_keys == secret.keys
        assert spec.insecure is False
