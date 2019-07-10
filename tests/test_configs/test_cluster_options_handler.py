import pytest

from conf.exceptions import ConfException
from conf.handlers.cluster_options_handler import ClusterOptionsHandler
from db.models.clusters import Cluster
from options.option import Option, OptionStores
from options.types import CONF_TYPES
from tests.base.case import BaseTest


class DummyDBOption(Option):
    key = 'FOO_BAR1'
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB_OPTION
    typing = CONF_TYPES.STR
    default = None
    options = None


class DummyOptionalDefaultDBOption(Option):
    key = 'FOO_BAR2'
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB_OPTION
    typing = CONF_TYPES.STR
    default = 'default_db'
    options = None


class DummyNonOptionalDBOption(Option):
    key = 'FOO_BAR3'
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.DB_OPTION
    typing = CONF_TYPES.STR
    default = None
    options = None


class DummySecretDBOption(Option):
    key = 'FOO_BAR4'
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.DB_OPTION
    typing = CONF_TYPES.STR
    default = None
    options = None


@pytest.mark.configs_mark
class TestClusterOptionsHandler(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Cluster.get_or_create_owner(Cluster.load())
        self.cluster_options_handler = ClusterOptionsHandler()

    def test_owner(self):
        assert self.cluster_options_handler.owner == self.owner

    def test_get_default_value(self):
        assert self.cluster_options_handler.get(DummyDBOption) is None
        assert self.cluster_options_handler.get(DummyOptionalDefaultDBOption) == 'default_db'
        with self.assertRaises(ConfException):
            self.cluster_options_handler.get(DummyNonOptionalDBOption)
        with self.assertRaises(ConfException):
            self.cluster_options_handler.get(DummySecretDBOption)

    def test_set_get_delete_value(self):
        self.cluster_options_handler.set(DummyDBOption, 123)
        self.cluster_options_handler.set(DummyOptionalDefaultDBOption, 123)
        self.cluster_options_handler.set(DummyNonOptionalDBOption, 123)
        self.cluster_options_handler.set(DummySecretDBOption, 123)

        assert self.cluster_options_handler.get(DummyDBOption) == 123
        assert self.cluster_options_handler.get(DummyOptionalDefaultDBOption) == 123
        assert self.cluster_options_handler.get(DummyNonOptionalDBOption) == 123
        assert self.cluster_options_handler.get(DummySecretDBOption) == 123

        self.cluster_options_handler.delete(DummyDBOption)
        self.cluster_options_handler.delete(DummyOptionalDefaultDBOption)
        self.cluster_options_handler.delete(DummyNonOptionalDBOption)
        self.cluster_options_handler.delete(DummySecretDBOption)

        assert self.cluster_options_handler.get(DummyDBOption) is None
        assert self.cluster_options_handler.get(DummyOptionalDefaultDBOption) == 'default_db'
        with self.assertRaises(ConfException):
            self.cluster_options_handler.get(DummyNonOptionalDBOption)
        with self.assertRaises(ConfException):
            self.cluster_options_handler.get(DummySecretDBOption)
