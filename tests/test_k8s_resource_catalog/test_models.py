import pytest

from django.db import IntegrityError

from db.models.clusters import Cluster
from db.models.config_maps import K8SConfigMap
from db.models.owner import Owner
from db.models.secrets import K8SSecret
from factories.factory_k8s_config_maps import K8SConfigMapFactory
from factories.factory_k8s_secrets import K8SSecretFactory
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


@pytest.mark.k8s_resource_catalog_mark
class TestK8SResourceModels(BaseTest):
    model_class = None
    factory_class = None

    def setUp(self):
        super().setUp()
        self.owner = Cluster.get_or_create_owner(Cluster.load())

    def test_has_owner(self):
        entity = self.factory_class()  # pylint:disable=not-callable
        self.assertEqual(entity.has_owner, True)

    def test_create_name_validation_raises_for_same_name(self):
        assert self.model_class.objects.count() == 0
        self.model_class.objects.create(owner=self.owner,
                                        name='k8s_name',
                                        k8s_ref='k8s_ref')
        with self.assertRaises(IntegrityError):
            self.model_class.objects.create(owner=self.owner,
                                            name='k8s_name',
                                            k8s_ref='k8s_ref')

    def test_create_name_validation_passes_for_different_owner(self):
        assert self.model_class.objects.count() == 0
        self.model_class.objects.create(owner=self.owner,
                                        name='k8s_name',
                                        k8s_ref='k8s_ref')
        assert self.model_class.objects.count() == 1
        # Using new owner with same name should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        self.model_class.objects.create(owner=owner,
                                        name='k8s_name',
                                        k8s_ref='k8s_ref')
        assert self.model_class.objects.count() == 2

    def test_same_ref_with_different_name_and_items(self):
        entity = self.model_class.objects.create(owner=self.owner,
                                                 name='k8s_name',
                                                 k8s_ref='k8s_ref')
        assert entity.owner == self.owner
        assert entity.name == 'k8s_name'
        assert entity.k8s_ref == 'k8s_ref'
        assert entity.items == []

        entity = self.model_class.objects.create(owner=self.owner,
                                                 name='k8s_name_with_items',
                                                 k8s_ref='k8s_ref',
                                                 items=['key1', 'key2'])
        assert entity.owner == self.owner
        assert entity.name == 'k8s_name_with_items'
        assert entity.k8s_ref == 'k8s_ref'
        assert entity.items == ['key1', 'key2']


@pytest.mark.k8s_resource_catalog_mark
class TestK8SConfigMapsModels(TestK8SResourceModels):
    model_class = K8SConfigMap
    factory_class = K8SConfigMapFactory


@pytest.mark.k8s_resource_catalog_mark
class TestK8SSecretsModels(TestK8SResourceModels):
    model_class = K8SSecret
    factory_class = K8SSecretFactory


del TestK8SResourceModels
