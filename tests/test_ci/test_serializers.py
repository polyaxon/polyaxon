import pytest

from api.ci.serializers import CISerializer
from db.models.ci import CI
from factories.ci_factory import CIFactory
from tests.utils import BaseTest


@pytest.mark.ci_mark
class TestCISerializer(BaseTest):
    serializer_class = CISerializer
    model_class = CI
    factory_class = CIFactory
    expected_keys = {'created_at', 'updated_at', 'config', }

    def setUp(self):
        super().setUp()
        self.obj1 = self.factory_class()
        self.obj1 = self.factory_class()

    def test_serialize_one(self):
        data = self.serializer_class(self.obj1).data

        assert set(data.keys()) == self.expected_keys
        data.pop('created_at')
        data.pop('updated_at')

        for k, v in data.items():
            assert getattr(self.obj1, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 2
        for d in data:
            assert set(d.keys()) == self.expected_keys
