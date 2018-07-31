from unittest.mock import patch

import pytest

from action_manager.actions.email import EMAIL_ACTION_EXECUTED, EmailAction
from tests.utils import BaseTest


# pylint:disable=protected-access

@pytest.mark.actions_mark
class TestEmailAction(BaseTest):
    DISABLE_RUNNER = True

    def test_attrs(self):
        assert EmailAction.action_key == 'email'
        assert EmailAction.name == 'Email'
        assert EmailAction.event_type == EMAIL_ACTION_EXECUTED

    def test_validate_config(self):
        assert EmailAction._validate_config({}) == {}
        assert EmailAction._validate_config({'foo': 'bar'}) == {}
        assert EmailAction._validate_config({
            'recipients': 'bar@gmail.com, foo@gmail.com'
        }) == {
                   'recipients': ['bar@gmail.com', 'foo@gmail.com']
               }
        assert EmailAction._validate_config({
            'recipients': ['bar@gmail.com', 'foo@gmail.com']
        }) == {
                   'recipients': ['bar@gmail.com', 'foo@gmail.com']
               }

    def test_get_config(self):
        assert EmailAction.get_config() == {}
        assert EmailAction.get_config({}) == {}
        assert EmailAction.get_config({'foo': 'bar'}) == {}
        assert EmailAction.get_config({
            'recipients': 'bar@gmail.com, foo@gmail.com'
        }) == {
                   'recipients': ['bar@gmail.com', 'foo@gmail.com']
               }
        assert EmailAction.get_config({
            'recipients': ['bar@gmail.com', 'foo@gmail.com']
        }) == {
                   'recipients': ['bar@gmail.com', 'foo@gmail.com']
               }

    def test_execute(self):
        with patch('action_manager.actions.email.send_mass_template_mail') as mock_execute:
            EmailAction.execute(context={})

        assert mock_execute.call_count == 0

        with patch('action_manager.actions.email.send_mass_template_mail') as mock_execute:
            EmailAction.execute(context=None,
                                config={'recipients': ['bar@gmail.com', 'foo@gmail.com']})

        assert mock_execute.call_count == 1
