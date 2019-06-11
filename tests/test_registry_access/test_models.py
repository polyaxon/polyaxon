import pytest

from django.db import IntegrityError

from db.models.clusters import Cluster
from db.models.owner import Owner
from db.models.registry_access import RegistryAccess
from db.models.secrets import K8SSecret
from factories.factory_registry_access import RegistryAccessFactory
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


@pytest.mark.registry_access_mark
class TestRegistryAccessModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_has_owner(self):
        regstry_access = RegistryAccessFactory()
        self.assertEqual(regstry_access.has_owner, True)

    def test_create_key_validation_raises_for_same_name(self):
        assert RegistryAccess.objects.count() == 0
        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='secret1',
                                          secret_ref='secret1')
        RegistryAccess.objects.create(owner=self.owner,
                                      name='my_registry',
                                      k8s_secret=secret)
        with self.assertRaises(IntegrityError):
            RegistryAccess.objects.create(owner=self.owner,
                                          name='my_registry',
                                          host='localhost:5000')

    def test_create_key_validation_passes_for_different_owner(self):
        assert RegistryAccess.objects.count() == 0
        RegistryAccess.objects.create(owner=self.owner, name='my_registry')
        assert RegistryAccess.objects.count() == 1
        # Using new owner with same keys should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        RegistryAccess.objects.create(owner=owner, name='my_registry')
        assert RegistryAccess.objects.count() == 2

    def test_same_registry_with_different_name_and_secret(self):
        registry = RegistryAccess.objects.create(owner=self.owner, name='my_registry')
        assert registry.owner == self.owner
        assert registry.name == 'my_registry'
        assert registry.k8s_secret is None
        assert registry.db_secret is None
        assert registry.host == ''

        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='secret1',
                                          secret_ref='secret1')
        registry = RegistryAccess.objects.create(owner=self.owner,
                                                 name='my_registry_with_secret_and_host',
                                                 k8s_secret=secret,
                                                 host='localhost:5000')
        assert registry.owner == self.owner
        assert registry.name == 'my_registry_with_secret_and_host'
        assert registry.k8s_secret == secret
        assert registry.db_secret is None
        assert registry.host == 'localhost:5000'
