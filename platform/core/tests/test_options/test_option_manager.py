import pytest

from options.option_manager import OptionManager
from options.registry.core import AdminViewEnabled, PasswordLength
from tests.base.case import BaseTest


@pytest.mark.options_mark
class TestOptionManager(BaseTest):
    def setUp(self):
        self.manager = OptionManager()
        super().setUp()

    def test_subscribe(self):
        self.assertEqual(len(self.manager.state), 0)
        self.manager.subscribe(AdminViewEnabled)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1
        assert AdminViewEnabled.key in self.manager.state
        assert self.manager.state[AdminViewEnabled.key] == AdminViewEnabled

        # Adding the same event
        self.manager.subscribe(AdminViewEnabled)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1

        # Adding new event
        self.manager.subscribe(PasswordLength)
        assert len(self.manager.state) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.keys) == 2
        assert len(self.manager.values) == 2

        # Adding new event with same event type
        class DummyEvent(PasswordLength):
            pass

        with self.assertRaises(AssertionError):
            self.manager.subscribe(DummyEvent)

    def test_knows(self):
        assert self.manager.knows(key=AdminViewEnabled.key) is False
        self.manager.subscribe(AdminViewEnabled)
        assert self.manager.knows(key=AdminViewEnabled.key) is True

        # Adding same event
        self.manager.subscribe(AdminViewEnabled)
        assert self.manager.knows(key=AdminViewEnabled.key) is True

        # New event
        assert self.manager.knows(PasswordLength) is False
        self.manager.subscribe(PasswordLength)
        assert self.manager.knows(key=PasswordLength.key) is True

    def test_get(self):
        assert self.manager.get(key=AdminViewEnabled.key) is None
        self.manager.subscribe(AdminViewEnabled)
        assert self.manager.get(key=AdminViewEnabled.key) == AdminViewEnabled
