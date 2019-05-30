import pytest

from django.db import IntegrityError

from db.models.clusters import Cluster
from db.models.config_maps import K8SConfigMap
from db.models.owner import Owner
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


@pytest.mark.config_maps_mark
class TestK8SConfigMapsModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_create_without_owner_raises(self):
        with self.assertRaises(IntegrityError):
            K8SConfigMap.objects.create(name='my_config', config_map_ref='my_config')

    def test_create_name_validation_raises_for_same_name(self):
        assert K8SConfigMap.objects.count() == 0
        K8SConfigMap.objects.create(owner=self.owner, name='my_config', config_map_ref='my_config')
        with self.assertRaises(IntegrityError):
            K8SConfigMap.objects.create(owner=self.owner,
                                        name='my_config',
                                        config_map_ref='my_config')

    def test_create_without_name(self):
        assert K8SConfigMap.objects.count() == 0
        K8SConfigMap.objects.create(owner=self.owner, config_map_ref='my_secret')
        assert K8SConfigMap.objects.count() == 1

    def test_create_name_validation_passes_for_different_owner(self):
        assert K8SConfigMap.objects.count() == 0
        K8SConfigMap.objects.create(owner=self.owner, name='my_config', config_map_ref='my_config')
        assert K8SConfigMap.objects.count() == 1
        # Using new owner with same name should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        K8SConfigMap.objects.create(owner=owner, name='my_config', config_map_ref='my_config')
        assert K8SConfigMap.objects.count() == 2

    def test_same_config_ref_with_different_name_and_keys(self):
        config = K8SConfigMap.objects.create(owner=self.owner,
                                             name='my_config',
                                             config_map_ref='my_config')
        assert config.owner == self.owner
        assert config.name == 'my_config'
        assert config.config_map_ref == 'my_config'
        assert config.keys == []

        config = K8SConfigMap.objects.create(owner=self.owner,
                                             name='my_config_with_keys',
                                             config_map_ref='my_config',
                                             keys=['key1', 'key2'])
        assert config.owner == self.owner
        assert config.name == 'my_config_with_keys'
        assert config.config_map_ref == 'my_config'
        assert config.keys == ['key1', 'key2']
