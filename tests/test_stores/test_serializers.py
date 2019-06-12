import pytest

from api.data_stores.serializers import DataStoreSerializer
from db.models.data_stores import DataStore
from factories.factory_data_stores import DataStoreFactory
from tests.base.case import BaseTest


@pytest.mark.stores_mark
class TestDataStoresSerializer(BaseTest):
    serializer_class = DataStoreSerializer
    model_class = DataStore
    factory_class = DataStoreFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'description',
        'readme',
        'tags',
        'created_at',
        'updated_at',
        'type',
        'mount_path',
        'host_path',
        'volume_claim',
        'bucket',
        'k8s_secret',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()
        self.obj1_query = DataStore.objects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(DataStore.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
