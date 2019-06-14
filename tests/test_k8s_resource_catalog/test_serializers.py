import pytest

from api.k8s_config_maps.serializers import K8SConfigMapSerializer, K8SConfigMapNameSerializer
from api.k8s_secrets.serializers import K8SSecretSerializer, K8SSecretNameSerializer
from db.models.config_maps import K8SConfigMap
from db.models.secrets import K8SSecret
from factories.factory_k8s_config_maps import K8SConfigMapFactory
from factories.factory_k8s_secrets import K8SSecretFactory
from tests.base.case import BaseTest


@pytest.mark.k8s_resource_catalog_mark
class TestK8SResourcesSerializer(BaseTest):
    serializer_class = None
    model_class = None
    factory_class = None
    expected_keys = {
        'id',
        'uuid',
        'name',
        'description',
        'readme',
        'tags',
        'created_at',
        'updated_at',
        'k8s_ref',
        'items',
    }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()  # pylint:disable=not-callable
        self.obj2 = self.factory_class()  # pylint:disable=not-callable
        self.obj1_query = self.model_class.objects.get(id=self.obj1.id)

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1_query).data    # pylint:disable=not-callable

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')
        assert data.pop('uuid') == self.obj1.uuid.hex

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(  # pylint:disable=not-callable
            self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys


@pytest.mark.k8s_resource_catalog_mark
class TestK8SResourcesNameSerializer(BaseTest):
    serializer_class = None
    model_class = None
    factory_class = None
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


@pytest.mark.k8s_resource_catalog_mark
class TestK8SConfigMapSerializer(TestK8SResourcesSerializer):
    serializer_class = K8SConfigMapSerializer
    model_class = K8SConfigMap
    factory_class = K8SConfigMapFactory


@pytest.mark.k8s_resource_catalog_mark
class TestK8SSecretSerializer(TestK8SResourcesSerializer):
    serializer_class = K8SSecretSerializer
    model_class = K8SSecret
    factory_class = K8SSecretFactory


@pytest.mark.k8s_resource_catalog_mark
class TestK8SConfigMapNameSerializer(TestK8SResourcesNameSerializer):
    serializer_class = K8SConfigMapNameSerializer
    model_class = K8SConfigMap
    factory_class = K8SConfigMapFactory


@pytest.mark.k8s_resource_catalog_mark
class TestK8SSecretNameSerializer(TestK8SResourcesNameSerializer):
    serializer_class = K8SSecretNameSerializer
    model_class = K8SSecret
    factory_class = K8SSecretFactory


del TestK8SResourcesSerializer
del TestK8SResourcesNameSerializer
