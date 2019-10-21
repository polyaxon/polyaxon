from unittest.mock import MagicMock

import pytest

import conf

from api.users.ldap_signals import populate_user_handler
from options.registry.email import EMAIL_DEFAULT_DOMAIN
from tests.base.case import BaseTest


@pytest.mark.users_mark
class TestAuthLdap(BaseTest):
    def test_populate_user(self):
        user = MagicMock()
        user.email = 'test@test.com'
        populate_user_handler(None, user=user, ldap_user=user.ldap_user)
        assert user.email == 'test@test.com'

        user = MagicMock()
        user.email = ''
        user.ldap_user.attrs = {'mail': ['test@test.com']}
        populate_user_handler(None, user=user, ldap_user=user.ldap_user)
        assert user.email == 'test@test.com'

        user = MagicMock()
        user.email = ''
        user.username = 'test'
        user.ldap_user.attrs = {}
        populate_user_handler(None, user=user, ldap_user=user.ldap_user)
        assert user.email == 'test@%s' % conf.get(EMAIL_DEFAULT_DOMAIN)
