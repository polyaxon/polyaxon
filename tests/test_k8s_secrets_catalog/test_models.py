import pytest

from django.db import IntegrityError

from db.models.clusters import Cluster
from db.models.owner import Owner
from db.models.secrets import K8SSecret
from factories.factory_k8s_secrets import K8SSecretFactory
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


@pytest.mark.secrets_catalog_mark
class TestK8SSecretsModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_has_owner(self):
        k8s_secret = K8SSecretFactory()
        self.assertEqual(k8s_secret.has_owner, True)

    def test_create_validation_raises_for_same_name(self):
        assert K8SSecret.objects.count() == 0
        K8SSecret.objects.create(owner=self.owner, name='my_secret', secret_ref='my_secret')
        with self.assertRaises(IntegrityError):
            K8SSecret.objects.create(owner=self.owner,
                                     name='my_secret',
                                     secret_ref='my_secret')

    def test_create_name_validation_passes_for_different_owner(self):
        assert K8SSecret.objects.count() == 0
        K8SSecret.objects.create(owner=self.owner, name='my_secret', secret_ref='my_secret')
        assert K8SSecret.objects.count() == 1
        # Using new owner with same name should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        K8SSecret.objects.create(owner=owner, name='my_secret', secret_ref='my_secret')
        assert K8SSecret.objects.count() == 2

    def test_same_secret_ref_with_different_name_and_keys(self):
        config = K8SSecret.objects.create(owner=self.owner,
                                          name='my_secret',
                                          secret_ref='my_secret')
        assert config.owner == self.owner
        assert config.name == 'my_secret'
        assert config.secret_ref == 'my_secret'
        assert config.keys == []

        config = K8SSecret.objects.create(owner=self.owner,
                                          name='my_secret_with_keys',
                                          secret_ref='my_secret',
                                          keys=['key1', 'key2'])
        assert config.owner == self.owner
        assert config.name == 'my_secret_with_keys'
        assert config.secret_ref == 'my_secret'
        assert config.keys == ['key1', 'key2']
