# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_cli.managers.auth import AuthConfigManager


def get_username_or_local(username):
    return username or AuthConfigManager.get_value('username')
