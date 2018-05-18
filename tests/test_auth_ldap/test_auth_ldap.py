# -*- coding: utf-8 -*-
from unittest.mock import MagicMock

from auth_ldap.signals import populate_user, DEFAULT_EMAIL_DOMAIN
from tests.utils import BaseTest


class TestAuthLdap(BaseTest):
    def test_populate_user(self):
        user = MagicMock()
        user.email = 'test@test.com'
        populate_user(None, user=user, ldap_user=user.ldap_user)
        assert user.email == 'test@test.com'

        user = MagicMock()
        user.email = ''
        user.ldap_user.attrs = {'mail': ['test@test.com']}
        populate_user(None, user=user, ldap_user=user.ldap_user)
        assert user.email == 'test@test.com'

        user = MagicMock()
        user.email = ''
        user.username = 'test'
        user.ldap_user.attrs = {}
        populate_user(None, user=user, ldap_user=user.ldap_user)
        assert user.email == 'test@%s' % DEFAULT_EMAIL_DOMAIN
