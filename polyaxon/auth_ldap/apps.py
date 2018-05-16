# -*- coding: utf-8 -*-
from django.apps import AppConfig


class AuthLdapConfig(AppConfig):
    name = 'auth_ldap'
    verbose_name = "AuthLdap"

    def ready(self):
        from .signals import (
            populate_user
        )