import pytest

from action_manager.action_event import ActionExecutedEvent
from action_manager.action_manager import ActionManager
from action_manager.actions.webhooks.pagerduty_webhook import PagerDutyWebHookAction
from action_manager.actions.webhooks.webhook import WebHookAction
from tests.utils import BaseTest


@pytest.mark.actions_mark
class TestActionManager(BaseTest):

    def setUp(self):
        self.manager = ActionManager()
        super().setUp()

    def test_subscribe(self):
        self.assertEqual(len(self.manager.state), 0)
        self.manager.subscribe(WebHookAction)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1
        assert WebHookAction.action_key in self.manager.state
        assert self.manager.state[WebHookAction.action_key] == WebHookAction

        # Adding the same event
        self.manager.subscribe(WebHookAction)
        assert len(self.manager.state) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.items) == 1
        assert len(self.manager.keys) == 1
        assert len(self.manager.values) == 1

        # Adding new event
        self.manager.subscribe(PagerDutyWebHookAction)
        assert len(self.manager.state) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.items) == 2
        assert len(self.manager.keys) == 2
        assert len(self.manager.values) == 2

        # Adding new event with same event type
        class DummyEvent(WebHookAction):
            pass

        with self.assertRaises(AssertionError):
            self.manager.subscribe(DummyEvent)

    def test_knows(self):
        assert self.manager.knows(action_key=WebHookAction.action_key) is False
        self.manager.subscribe(WebHookAction)
        assert self.manager.knows(action_key=WebHookAction.action_key) is True

        # Adding same event
        self.manager.subscribe(WebHookAction)
        assert self.manager.knows(action_key=WebHookAction.action_key) is True

        # New event
        assert self.manager.knows(PagerDutyWebHookAction) is False
        self.manager.subscribe(PagerDutyWebHookAction)
        assert self.manager.knows(action_key=PagerDutyWebHookAction.action_key) is True

    def test_get(self):
        assert self.manager.get(action_key=WebHookAction.action_key) is None
        self.manager.subscribe(WebHookAction)
        assert self.manager.get(action_key=WebHookAction.action_key) == WebHookAction

    def test_action_event(self):
        assert len(ActionExecutedEvent.attributes) == 2
        assert ActionExecutedEvent.attributes[0].name == 'automatic'
        assert ActionExecutedEvent.attributes[1].name == 'user.id'
