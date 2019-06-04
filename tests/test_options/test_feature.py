import pytest

from options.exceptions import OptionException
from options.feature import Feature
from options.option import OptionStores, NAMESPACE_DB_OPTION_MARKER
from tests.base.case import BaseTest


class DummyFeature(Feature):
    pass


@pytest.mark.options_mark
class TestFeature(BaseTest):

    def test_feature_default_store(self):
        assert DummyFeature.store == OptionStores.DB_OPTION

    def test_feature_marker(self):
        assert DummyFeature.get_marker() == NAMESPACE_DB_OPTION_MARKER

    def test_parse_key_wtong_namespace(self):
        DummyFeature.key = 'FOO'

        with self.assertRaises(OptionException):
            DummyFeature.parse_key()

        DummyFeature.key = 'FOO:BAR'

        with self.assertRaises(OptionException):
            DummyFeature.parse_key()

    def test_parse_key_without_namespace(self):
        DummyFeature.key = 'FEATURES:FOO'

        assert DummyFeature.parse_key() == (None, 'FOO')

    def test_parse_key_with_namespace(self):
        DummyFeature.key = 'FEATURES:FOO:BAR'

        assert DummyFeature.parse_key() == ('FOO', 'BAR')
