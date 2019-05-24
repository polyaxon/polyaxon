import pytest
from django.db import IntegrityError

from db.models.artifacts_stores import ArtifactsStore
from db.models.clusters import Cluster
from db.models.config_maps import K8SConfigMap
from db.models.configs import Config
from db.models.data_stores import DataStore
from db.models.logs_stores import LogsStore
from db.models.owner import Owner
from db.models.secrets import K8SSecret
from tests.base.case import BaseTest


@pytest.mark.configs_mark
class TestConfigModel(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_create_default_config_for_cluster(self):
        assert Config.objects.count() == 0

        k8s_config_map = K8SConfigMap.objects.create(owner=self.owner,
                                                     name='my_config',
                                                     config_map_ref='my_config')
        k8s_secret = K8SSecret.objects.create(owner=self.owner,
                                              name='my_secret',
                                              secret_ref='my_secret')

        dataset1 = DataStore.objects.create(owner=self.owner,
                                            name='data1',
                                            host_path='/tmp/foo',
                                            mount_path='/data1')
        dataset2 = DataStore.objects.create(owner=self.owner,
                                            name='data2',
                                            volume_claim='foo',
                                            mount_path='/data2')

        outputs = ArtifactsStore.objects.create(owner=self.owner,
                                                name='outputs1',
                                                host_path='/tmp/outputs',
                                                mount_path='/outputs1')

        logs = LogsStore.objects.create(owner=self.owner,
                                        name='logs1',
                                        bucket='some_bucket')
        config = Config.objects.create(owner=self.owner, artifacts=outputs, logs=logs)
        config.datasets.add(dataset1, dataset2)
        config.k8s_config_maps.add(k8s_config_map)
        config.k8s_secrets.add(k8s_secret)

        assert Config.objects.count() == 1

        config = Config.objects.last()

        assert config.owner == self.owner
        assert config.artifacts == outputs
        assert config.logs == logs
        assert list(config.datasets.all()) == [dataset1, dataset2]
        assert list(config.k8s_config_maps.all()) == [k8s_config_map]
        assert list(config.k8s_secrets.all()) == [k8s_secret]

        # Creating another config should raise
        with self.assertRaises(IntegrityError):
            Config.objects.create(owner=self.owner, artifacts=outputs)
