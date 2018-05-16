# -*- coding: utf-8 -*-
import ldap
from django_auth_ldap.config import LDAPSearch

from polyaxon.utils import config
from .apps import INSTALLED_APPS

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

if config.get_boolean('POLYAXON_AUTH_LDAP', is_optional=True):
    AUTHENTICATION_BACKENDS = ['django_auth_ldap.backend.LDAPBackend'] + AUTHENTICATION_BACKENDS

    AUTH_LDAP_SERVER_URI = config.get_string('POLYAXON_AUTH_LDAP_SERVER_URI')

    AUTH_LDAP_BIND_DN = config.get_string('POLYAXON_AUTH_LDAP_BIND_DN', is_optional=True)
    AUTH_LDAP_BIND_PASSWORD = config.get_string('POLYAXON_AUTH_LDAP_BIND_PASSWORD', is_optional=True)
    base_dn = config.get_string('POLYAXON_AUTH_LDAP_USER_SEARCH_BASE_DN', is_optional=True)
    filterstr = config.get_string('POLYAXON_AUTH_LDAP_USER_SEARCH_FILTERSTR', is_optional=True)
    AUTH_LDAP_USER_SEARCH = LDAPSearch(base_dn, ldap.SCOPE_SUBTREE, filterstr)
    AUTH_LDAP_CONNECTION_OPTIONS = {
        ldap.OPT_NETWORK_TIMEOUT: 3
    }
    AUTH_LDAP_USER_DN_TEMPLATE = config.get_string('POLYAXON_AUTH_LDAP_USER_DN_TEMPLATE', is_optional=True)

    INSTALLED_APPS += ('auth_ldap.apps.AuthLdapConfig',)
