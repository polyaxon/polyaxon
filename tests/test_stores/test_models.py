import pytest

from django.db import IntegrityError

from db.models.artifacts_stores import ArtifactsStore
from db.models.clusters import Cluster
from db.models.data_stores import DataStore
from db.models.logs_stores import LogsStore
from db.models.owner import Owner
from db.models.secrets import K8SSecret
from factories.factory_artifacts_stores import ArtifactsStoreFactory
from factories.factory_data_stores import DataStoreFactory
from factories.factory_logs_stores import LogsStoreFactory
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


class BaseStoreTest(BaseTest):
    model_class = None
    factory_class = None

    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_has_owner(self):
        obj = self.factory_class()  # pylint:disable=not-callable
        self.assertEqual(obj.has_owner, True)

    def test_create_key_validation_raises_for_same_name(self):
        assert self.model_class.objects.count() == 0
        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='secret1',
                                          k8s_ref='secret1')
        self.model_class.objects.create(owner=self.owner,
                                        name='my_store',
                                        host_path='/tmp/foo',
                                        mount_path='/tmp/foo',
                                        k8s_secret=secret)
        with self.assertRaises(IntegrityError):
            self.model_class.objects.create(owner=self.owner,
                                            name='my_store')

    def test_create_key_validation_passes_for_different_owner(self):
        assert self.model_class.objects.count() == 0
        self.model_class.objects.create(owner=self.owner, name='my_store')
        assert self.model_class.objects.count() == 1
        # Using new owner with same keys should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        self.model_class.objects.create(owner=owner, name='my_store')
        assert self.model_class.objects.count() == 2

    def test_same_store_with_different_name_and_secret(self):
        registry = self.model_class.objects.create(owner=self.owner,
                                                   volume_claim='foo',
                                                   mount_path='/tmp/foo',
                                                   name='my_store')
        assert registry.owner == self.owner
        assert registry.name == 'my_store'
        assert registry.volume_claim == 'foo'
        assert registry.mount_path == '/tmp/foo'
        assert registry.bucket is None
        assert registry.host_path is None
        assert registry.db_secret is None
        assert registry.k8s_secret is None
        assert registry.read_only is False

        secret = K8SSecret.objects.create(owner=self.owner,
                                          name='my_store',
                                          k8s_ref='my_store')
        registry = self.model_class.objects.create(owner=self.owner,
                                                   name='my_store_with_secret_and_host',
                                                   k8s_secret=secret,
                                                   bucket='s3.bucket')
        assert registry.owner == self.owner
        assert registry.name == 'my_store_with_secret_and_host'

        assert registry.name == 'my_store_with_secret_and_host'
        assert registry.volume_claim is None
        assert registry.mount_path is None
        assert registry.bucket == 's3.bucket'
        assert registry.host_path is None
        assert registry.db_secret is None
        assert registry.k8s_secret == secret


@pytest.mark.stores_mark
class TestDataStoreModels(BaseStoreTest):
    model_class = DataStore
    factory_class = DataStoreFactory


@pytest.mark.stores_mark
class TestArtifactsStoreModels(BaseStoreTest):
    model_class = ArtifactsStore
    factory_class = ArtifactsStoreFactory


@pytest.mark.stores_mark
class TestLogsStoreModels(BaseStoreTest):
    model_class = LogsStore
    factory_class = LogsStoreFactory


del BaseStoreTest
