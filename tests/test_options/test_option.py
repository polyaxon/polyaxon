import pytest

from options.exceptions import OptionException
from options.option import Option, OptionStores, NAMESPACE_DB_OPTION_MARKER, \
    NAMESPACE_DB_CONFIG_MARKER, NAMESPACE_SETTINGS_MARKER, NAMESPACE_ENV_MARKER
from tests.base.case import BaseTest


class DummyOption(Option):
    pass


@pytest.mark.options_mark
class TestOption(BaseTest):

    def test_option_marker(self):
        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.get_marker() == NAMESPACE_DB_OPTION_MARKER

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.get_marker() == NAMESPACE_DB_CONFIG_MARKER

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.get_marker() == NAMESPACE_SETTINGS_MARKER

        DummyOption.store = OptionStores.ENV
        assert DummyOption.get_marker() == NAMESPACE_ENV_MARKER

    def test_parse_key_without_namespace(self):
        DummyOption.key = 'FOO'

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == (None, 'FOO')

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == (None, 'FOO')

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == (None, 'FOO')

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == (None, 'FOO')

    def test_parse_key_with_namespace(self):
        DummyOption.key = 'FOO:BAR'

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == ('FOO', 'BAR')

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == (None, 'FOO:BAR')

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == (None, 'FOO:BAR')

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == (None, 'FOO:BAR')

        DummyOption.key = 'FOO__BAR'

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == (None, 'FOO__BAR')

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == ('FOO', 'BAR')

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == ('FOO', 'BAR')

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == ('FOO', 'BAR')

    def test_parse_key_wrong_namespace(self):
        DummyOption.key = 'FOO:BAR:MOO'

        DummyOption.store = OptionStores.DB_OPTION
        with self.assertRaises(OptionException):
            DummyOption.parse_key()

        DummyOption.store = OptionStores.DB_CONFIG
        assert DummyOption.parse_key() == (None, 'FOO:BAR:MOO')

        DummyOption.store = OptionStores.SETTINGS
        assert DummyOption.parse_key() == (None, 'FOO:BAR:MOO')

        DummyOption.store = OptionStores.ENV
        assert DummyOption.parse_key() == (None, 'FOO:BAR:MOO')

        DummyOption.key = 'FOO__BAR__MOO'

        DummyOption.store = OptionStores.DB_OPTION
        assert DummyOption.parse_key() == (None, 'FOO__BAR__MOO')

        DummyOption.store = OptionStores.DB_CONFIG
        with self.assertRaises(OptionException):
            DummyOption.parse_key()

        DummyOption.store = OptionStores.SETTINGS
        with self.assertRaises(OptionException):
            DummyOption.parse_key()

        DummyOption.store = OptionStores.ENV
        with self.assertRaises(OptionException):
            DummyOption.parse_key()



