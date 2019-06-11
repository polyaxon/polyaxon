import pytest

from api.options.serializers import ConfigOptionSerializer
from db.models.clusters import Cluster
from db.models.config_options import ConfigOption
from db.models.owner import Owner
from tests.base.case import BaseTest


@pytest.mark.configs_mark
class TestConfigOptionSerializer(BaseTest):
    serializer_class = ConfigOptionSerializer
    model_class = ConfigOption
    expected_keys = {
        'key',
        'option',
        'is_secret',
    }

    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)
        self.option_value1 = ConfigOption.objects.create(owner=self.owner,
                                                         key='value1',
                                                         value=2341)
        self.option_value2 = ConfigOption.objects.create(owner=self.owner,
                                                         key='value2',
                                                         value={'foo': 'bar'})
        self.option_secret1 = ConfigOption.objects.create(owner=self.owner,
                                                          key='secret1',
                                                          secret='secret1')
        self.option_secret2 = ConfigOption.objects.create(owner=self.owner,
                                                          key='secret2',
                                                          secret='secret2')

    def test_serialize_one(self):
        data = self.serializer_class(self.option_value1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('option') == self.option_value1.value
        for k, v in data.items():
            assert getattr(self.option_value1, k) == v

        data = self.serializer_class(self.option_value2).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('option') == self.option_value2.value
        for k, v in data.items():
            assert getattr(self.option_value2, k) == v

        data = self.serializer_class(self.option_secret1).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('option') == self.option_secret1.secret
        for k, v in data.items():
            assert getattr(self.option_secret1, k) == v

        data = self.serializer_class(self.option_secret2).data

        assert set(data.keys()) == self.expected_keys
        assert data.pop('option') == self.option_secret2.secret
        for k, v in data.items():
            assert getattr(self.option_secret2, k) == v

    def test_serialize_many(self):
        data = self.serializer_class(self.model_class.objects.all(), many=True).data
        assert len(data) == 4
        for d in data:
            assert set(d.keys()) == self.expected_keys
