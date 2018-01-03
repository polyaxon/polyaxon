# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Users'

    def ready(self):
        from users.signals import create_auth_token
