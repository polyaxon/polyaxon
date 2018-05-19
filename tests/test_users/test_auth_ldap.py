# -*- coding: utf-8 -*-
from unittest.mock import MagicMock

from django.conf import settings

from tests.utils import BaseTest
from users.ldap_signals import populate_user_handler


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
        assert user.email == 'test@%s' % settings.DEFAULT_EMAIL_DOMAIN
