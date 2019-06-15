import pytest

from api.registry_access.serializers import RegistryAccessNameSerializer, RegistryAccessSerializer
from db.models.registry_access import RegistryAccess
from factories.factory_registry_access import RegistryAccessFactory
from tests.base.case import BaseTest


@pytest.mark.registry_access_mark
class TestRegistryAccessSerializer(BaseTest):
    serializer_class = RegistryAccessSerializer
    model_class = RegistryAccess
    factory_class = RegistryAccessFactory
    expected_keys = {
        'id',
        'uuid',
        'name',
        'description',
        'readme',
        'tags',
        'created_at',
        'updated_at',
        'k8s_secret',
        'host',
        'is_default'
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj2 = self.factory_class()
        self.obj1_query = RegistryAccess.objects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex
        assert data.pop('is_default') is False

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(RegistryAccess.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.registry_access_mark
class TestRegistryAccessNameSerializer(BaseTest):
    serializer_class = RegistryAccessNameSerializer
    model_class = RegistryAccess
    factory_class = RegistryAccessFactory
    expected_keys = {
        'id',
        'name',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()  # pylint:disable=not-callable
        self.obj2 = self.factory_class()  # pylint:disable=not-callable

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
