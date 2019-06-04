import pytest

from django.db import IntegrityError

from db.models.clusters import Cluster
from db.models.config_options import ConfigOption
from db.models.owner import Owner
from factories.factory_users import UserFactory
from tests.base.case import BaseTest


@pytest.mark.configs_mark
class TestConfigOptionModels(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)

    def test_create_without_owner_raises(self):
        with self.assertRaises(IntegrityError):
            ConfigOption.objects.create(key='int2', value=-2341)

    def test_create_int(self):
        assert ConfigOption.objects.count() == 0

        ConfigOption.objects.create(owner=self.owner, key='int1', value=1)
        assert ConfigOption.objects.count() == 1
        assert ConfigOption.objects.last().value == 1
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner, key='int2', value=-2341)
        assert ConfigOption.objects.count() == 2
        assert ConfigOption.objects.last().value == -2341
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner, key='int3', secret=1)
        assert ConfigOption.objects.count() == 3
        assert ConfigOption.objects.last().secret == 1
        assert ConfigOption.objects.last().value is None

        ConfigOption.objects.create(owner=self.owner, key='int4', secret=-2341)
        assert ConfigOption.objects.count() == 4
        assert ConfigOption.objects.last().secret == -2341
        assert ConfigOption.objects.last().value is None

    def test_create_float(self):
        assert ConfigOption.objects.count() == 0

        ConfigOption.objects.create(owner=self.owner, key='float1', value=1.1)
        assert ConfigOption.objects.count() == 1
        assert ConfigOption.objects.last().value == 1.1
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner, key='float2', value=-2341.234)
        assert ConfigOption.objects.count() == 2
        assert ConfigOption.objects.last().value == -2341.234
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner, key='float3', secret=1.34)
        assert ConfigOption.objects.count() == 3
        assert ConfigOption.objects.last().secret == 1.34
        assert ConfigOption.objects.last().value is None

        ConfigOption.objects.create(owner=self.owner, key='float4', secret=-2341.34)
        assert ConfigOption.objects.count() == 4
        assert ConfigOption.objects.last().secret == -2341.34
        assert ConfigOption.objects.last().value is None

    def test_create_str(self):
        assert ConfigOption.objects.count() == 0

        ConfigOption.objects.create(owner=self.owner, key='str1', value='sdf')
        assert ConfigOption.objects.count() == 1
        assert ConfigOption.objects.last().value == 'sdf'
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner, key='str2', value='2341')
        assert ConfigOption.objects.count() == 2
        assert ConfigOption.objects.last().value == '2341'
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner, key='str3', secret='foo')
        assert ConfigOption.objects.count() == 3
        assert ConfigOption.objects.last().secret == 'foo'
        assert ConfigOption.objects.last().value is None

    def test_create_dict(self):
        assert ConfigOption.objects.count() == 0

        ConfigOption.objects.create(owner=self.owner, key='dict1', value={"A": "B", "123": "123"})
        assert ConfigOption.objects.count() == 1
        assert ConfigOption.objects.last().value == {"A": "B", "123": "123"}
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner,
                                    key='dict2',
                                    value={"A": "B", "new": ["123", 123, {"nested": "nested"}]})
        assert ConfigOption.objects.count() == 2
        assert ConfigOption.objects.last().value == {"A": "B",
                                                     "new": ["123", 123, {"nested": "nested"}]}
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner,
                                    key='dict3',
                                    secret={"A": "B", "new": ["123", 123, {"nested": "nested"}]})
        assert ConfigOption.objects.count() == 3
        assert ConfigOption.objects.last().secret == {"A": "B",
                                                      "new": ["123", 123, {"nested": "nested"}]}
        assert ConfigOption.objects.last().value is None

    def test_create_list(self):
        assert ConfigOption.objects.count() == 0

        ConfigOption.objects.create(owner=self.owner,
                                    key='dict1',
                                    value=["A", "B", "123", {"foo": "123"}])
        assert ConfigOption.objects.count() == 1
        assert ConfigOption.objects.last().value == ["A", "B", "123", {"foo": "123"}]
        assert ConfigOption.objects.last().secret is None

        ConfigOption.objects.create(owner=self.owner,
                                    key='dict3',
                                    secret=["A", "B", "123", {"foo": "123"}])
        assert ConfigOption.objects.count() == 2
        assert ConfigOption.objects.last().secret == ["A", "B", "123", {"foo": "123"}]
        assert ConfigOption.objects.last().value is None

    def test_create_key_validation_raises_for_same_key(self):
        assert ConfigOption.objects.count() == 0
        ConfigOption.objects.create(owner=self.owner, key='key', value="foo")
        with self.assertRaises(IntegrityError):
            ConfigOption.objects.create(owner=self.owner, key='key', value="bar")

    def test_create_key_validation_passes_for_different_owner(self):
        assert ConfigOption.objects.count() == 0
        ConfigOption.objects.create(owner=self.owner, key='key', value="foo")
        assert ConfigOption.objects.count() == 1
        # Using new owner with same keys should work
        user = UserFactory()  # Creates a new owner
        owner = Owner.objects.get(name=user.username)
        ConfigOption.objects.create(owner=owner, key='key', value="bar")
        assert ConfigOption.objects.count() == 2
