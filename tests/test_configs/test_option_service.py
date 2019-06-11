import pytest

from django.conf import settings

from conf.cluster_conf_service import ClusterConfService
from conf.exceptions import ConfException
from conf.service import ConfService
from db.models.clusters import Cluster
from db.models.config_options import ConfigOption
from db.models.owner import Owner
from options.option import Option, OptionStores
from options.option_manager import OptionManager
from options.types import CONF_TYPES
from tests.base.case import BaseTest


class DummySettingsService(ConfService):

    def __init__(self):
        self.options = set([])
        super().__init__()

    def get(self, key, to_dict=False):
        self.options.add(key)
        return super().get(key, to_dict=to_dict)


class DummyDBService(ClusterConfService):

    def __init__(self):
        self.options = set([])
        super().__init__()

    def get(self, key, to_dict=False):
        self.options.add(key)
        return super().get(key, to_dict=to_dict)


class DummySettingsOption(Option):
    key = 'FOO_BAR'
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class DummyOptionalDefaultSettingsOption(Option):
    key = 'FOO_BAR2'
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = 'default_settings'
    options = None


class DummyNonOptionalSettingsOption(Option):
    key = 'FOO_BAR2'
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class DummyDBOption(Option):
    key = 'FOO_BAR'
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB_OPTION
    typing = None
    default = None
    options = None


class DummyOptionalDefaultDBOption(Option):
    key = 'FOO_BAR2'
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB_OPTION
    typing = None
    default = 'default_db'
    options = None


class DummyNonOptionalDBOption(Option):
    key = 'FOO_BAR2'
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.DB_OPTION
    typing = None
    default = None
    options = None


@pytest.mark.configs_mark
class TestConfService(BaseTest):
    def setUp(self):
        super().setUp()
        self.owner = Owner.objects.get(name=Cluster.load().uuid)
        self.settings_service = DummySettingsService()
        self.db_service = DummyDBService()
        self.settings_service.option_manager = OptionManager()
        self.db_service.option_manager = OptionManager()
        self.settings_service.setup()
        self.db_service.setup()

    def test_can_handle(self):
        # Test handles only str event types
        assert self.settings_service.can_handle(key=1) is False

        # The service's manager did not subscribe to the event yet
        assert self.settings_service.can_handle(key=DummySettingsOption.key) is False

        # Subscribe to the event
        self.settings_service.option_manager.subscribe(DummySettingsOption)
        assert self.settings_service.can_handle(key=DummySettingsOption.key) is True

    def test_non_optional_settings(self):
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummyNonOptionalSettingsOption.key)
        # Subscribe to the event
        self.settings_service.option_manager.subscribe(DummyNonOptionalSettingsOption)
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummyNonOptionalSettingsOption.key)

    def test_non_optional_db(self):
        with self.assertRaises(ConfException):
            self.db_service.get(key=DummyNonOptionalDBOption.key)
        # Subscribe to the event
        self.db_service.option_manager.subscribe(DummyNonOptionalDBOption)
        with self.assertRaises(ConfException):
            self.db_service.get(key=DummyNonOptionalDBOption.key)

    def test_optional_with_default_settings(self):
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummyOptionalDefaultSettingsOption.key)
        # Subscribe to the event
        self.settings_service.option_manager.subscribe(DummyOptionalDefaultSettingsOption)
        assert self.settings_service.get(
            key=DummyOptionalDefaultSettingsOption.key) == 'default_settings'

    def test_optional_with_default_db(self):
        with self.assertRaises(ConfException):
            self.db_service.get(key=DummyOptionalDefaultDBOption.key)
        # Subscribe to the event
        self.db_service.option_manager.subscribe(DummyOptionalDefaultDBOption)
        assert self.db_service.get(
            key=DummyOptionalDefaultDBOption.key) == 'default_db'

    def test_get_from_settings(self):
        settings.FOO_BAR = None
        # The service's manager did not subscribe to the event yet
        with self.assertRaises(ConfException):
            self.settings_service.get(key=DummySettingsOption.key)

        # Subscribe
        self.settings_service.option_manager.subscribe(DummySettingsOption)

        # No entry in settings
        assert self.settings_service.get(key=DummySettingsOption.key) is None

        # Update settings
        settings.FOO_BAR = 'foo'
        assert self.settings_service.get(key=DummySettingsOption.key) == 'foo'

        # Get as option
        option_dict = DummySettingsOption.to_dict(value='foo')
        assert option_dict['value'] == 'foo'
        assert self.settings_service.get(key=DummySettingsOption.key, to_dict=True) == option_dict

        assert len(self.settings_service.options) == 1
        option_key = self.settings_service.options.pop()
        assert option_key == DummySettingsOption.key

    def test_get_from_db(self):
        # The service's manager did not subscribe to the event yet
        with self.assertRaises(ConfException):
            self.db_service.get(key=DummyDBOption.key)

        # Subscribe
        self.db_service.option_manager.subscribe(DummyDBOption)

        # No entry in db
        assert self.db_service.get(key=DummyDBOption.key) is None

        # Update settings does not change anything
        settings.FOO_BAR = 'foo'
        assert self.db_service.get(key=DummyDBOption.key) is None

        # Update db
        ConfigOption.objects.create(owner=self.owner, key=DummyDBOption.key, value='foo')
        assert self.db_service.get(key=DummyDBOption.key) == 'foo'

        # Get as option
        option_dict = DummyDBOption.to_dict(value='foo')
        assert option_dict['value'] == 'foo'
        assert self.db_service.get(key=DummyDBOption.key, to_dict=True) == option_dict

        assert len(self.db_service.options) == 1
        option_key = self.db_service.options.pop()
        assert option_key == DummyDBOption.key

    def test_setting_none_value_raises(self):
        with self.assertRaises(ConfException):
            self.settings_service.set(key='SOME_NEW_KEY', value=None)

        with self.assertRaises(ConfException):
            self.db_service.set(key='SOME_NEW_KEY', value=None)

    def test_setting_unknown_key_raises(self):
        with self.assertRaises(ConfException):
            self.settings_service.set(key='SOME_NEW_KEY', value='foo_bar')

        with self.assertRaises(ConfException):
            self.db_service.set(key='SOME_NEW_KEY', value='foo_bar')

    def test_cannot_set_keys_on_settings_backend(self):
        with self.assertRaises(ConfException):
            self.settings_service.set(key=DummySettingsOption.key, value='foo_bar')

        # Subscribe
        self.settings_service.option_manager.subscribe(DummySettingsOption)

        with self.assertRaises(ConfException):
            self.settings_service.set(key=DummySettingsOption.key, value='foo_bar')

    def test_cannot_delete_keys_on_settings_backend(self):
        with self.assertRaises(ConfException):
            self.settings_service.delete(key=DummySettingsOption.key)

        # Subscribe
        self.settings_service.option_manager.subscribe(DummySettingsOption)

        with self.assertRaises(ConfException):
            self.settings_service.delete(key=DummySettingsOption.key)
