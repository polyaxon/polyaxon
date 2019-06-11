import pytest

from api.k8s_config_maps.serializers import K8SConfigMapSerializer
from db.models.config_maps import K8SConfigMap
from factories.factory_k8s_config_maps import K8SConfigMapFactory
from tests.base.case import BaseTest


@pytest.mark.config_maps_catalog_mark
class TestK8SConfigMapsSerializer(BaseTest):
    serializer_class = K8SConfigMapSerializer
    model_class = K8SConfigMap
    factory_class = K8SConfigMapFactory
    expected_keys = {
        'uuid',
        'name',
        'description',
        'readme',
        'keys',
        'tags',
        'created_at',
        'updated_at',
        'config_map_ref',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()
        self.obj1_query = K8SConfigMap.objects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(K8SConfigMap.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
