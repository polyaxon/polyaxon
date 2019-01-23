# pylint:disable=protected-access
from unittest.mock import patch

import pytest

from django.test import override_settings

from action_manager.actions.email import EMAIL_ACTION_EXECUTED, EmailAction
from tests.utils import BaseTest


@pytest.mark.actions_mark
class TestEmailAction(BaseTest):

    def test_attrs(self):
        assert EmailAction.action_key == 'email'
        assert EmailAction.name == 'Email'
        assert EmailAction.event_type == EMAIL_ACTION_EXECUTED

    def test_validate_config(self):
        assert EmailAction._validate_config({}) == {}
        assert EmailAction._validate_config({'foo': 'bar'}) == {}
        assert EmailAction._validate_config({
            'recipients': 'bar@gmail.com, foo@gmail.com'
        }) == {'recipients': ['bar@gmail.com', 'foo@gmail.com']}
        assert EmailAction._validate_config({
            'recipients': ['bar@gmail.com', 'foo@gmail.com']
        }) == {'recipients': ['bar@gmail.com', 'foo@gmail.com']}

    def test_get_config(self):
        assert EmailAction.get_config() == {}
        assert EmailAction.get_config({}) == {}
        assert EmailAction.get_config({'foo': 'bar'}) == {}
        assert EmailAction.get_config({
            'recipients': 'bar@gmail.com, foo@gmail.com'
        }) == {'recipients': ['bar@gmail.com', 'foo@gmail.com']}
        assert EmailAction.get_config({
            'recipients': ['bar@gmail.com', 'foo@gmail.com']
        }) == {'recipients': ['bar@gmail.com', 'foo@gmail.com']}

    def test_execute_no_settings(self):
        with patch('action_manager.actions.email.send_mass_template_mail') as mock_execute:
            EmailAction.execute(context={})

        assert mock_execute.call_count == 0

        with patch('action_manager.actions.email.send_mass_template_mail') as mock_execute:
            EmailAction.execute(context=None,
                                config={'recipients': ['bar@gmail.com', 'foo@gmail.com']})

        assert mock_execute.call_count == 0

    @override_settings(EMAIL_HOST_USER='foo', EMAIL_HOST_PASSWORD='bar')
    def test_execute(self):
        with patch('action_manager.actions.email.send_mass_template_mail') as mock_execute:
            EmailAction.execute(context={})

        assert mock_execute.call_count == 0

        with patch('action_manager.actions.email.send_mass_template_mail') as mock_execute:
            EmailAction.execute(context=None,
                                config={'recipients': ['bar@gmail.com', 'foo@gmail.com']})

        assert mock_execute.call_count == 1
