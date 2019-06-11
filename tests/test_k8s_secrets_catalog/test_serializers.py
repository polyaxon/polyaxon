import pytest

from api.k8s_secrets.serializers import K8SSecretSerializer
from db.models.secrets import K8SSecret
from factories.factory_k8s_secrets import K8SSecretFactory
from tests.base.case import BaseTest


@pytest.mark.secrets_catalog_mark
class TestK8SConfigMapsSerializer(BaseTest):
    serializer_class = K8SSecretSerializer
    model_class = K8SSecret
    factory_class = K8SSecretFactory
    expected_keys = {
        'uuid',
        'name',
        'description',
        'readme',
        'keys',
        'tags',
        'created_at',
        'updated_at',
        'secret_ref',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()
        self.obj1_query = K8SSecret.objects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(K8SSecret.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
